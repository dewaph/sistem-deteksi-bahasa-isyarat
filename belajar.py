import streamlit as st
import mysql.connector
from PIL import Image
import io
from moviepy.editor import *

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistem_deteksi_isyarat"
    )

def resize_image(image, size):
    resized_image = image.resize(size)
    return resized_image

def app():
    st.markdown("""
                            <style>
                            div.stButton > button:first-child {
                            font-family: Hack, monospace;
                            background: #C41F1E;
                            color: white;
                            cursor: pointer;
                            font-size: 2em;
                            padding: 0.5rem;
                            border: 0;
                            transition: all 0.5s;
                            border-radius: 10px;
                            width: auto;
                            position: relative;
                            min-width: 100px;

                            &::after {
                            font-weight: 400;
                            position: absolute;
                            left: 80%;
                            top: 54%;
                            right: 0;
                            bottom: 0;
                            opacity: 0;
                            transform: translate(-50%, -50%);
                            } 

                            &:hover {
                    	        background: #026633;
                                transition: all 0.5s;
                                border-radius: 10px;
                                box-shadow: 0px 6px 15px #0000ff61;
                                color: #ffffff;

                                &::after {
                                opacity: 1;
                                transition: all 0.5s;
                                color: #ffffff;
                            }
                            }}
                            </style>""", unsafe_allow_html=True)
    st.title('Belajar Huruf Alfabet Isyarat')
    st.header('BISINDO')

    user_input = st.text_input("Masukkan teks atau kata:", "").upper()

    connection = get_db_connection()
    cursor = connection.cursor()

    if not user_input:
        query = "SELECT kamus.letter, image_data, video_data FROM kamus LEFT JOIN image_table ON kamus.image_data_id = image_table.id LEFT JOIN video_table ON kamus.video_data_id = video_table.id ORDER BY kamus.letter ASC; "
        cursor.execute(query)
        results = cursor.fetchall()

        alphabet_set = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        for letter in sorted(alphabet_set):
            st.header(f'{letter}')

            col1, col2 = st.columns(2)

            found_letter_data = False

            for result in results:
                db_letter, image_data, video_data = result

                if db_letter == letter:
                    found_letter_data = True

                    with col1:
                        if image_data:
                            image = Image.open(io.BytesIO(image_data))
                            resized_image = resize_image(image, (200, 200))
                            st.image(resized_image, width=150)

                    if video_data:
                        if st.button(f"Tampilkan Video {letter}", key=f"video_{letter}"):
                            video_file = io.BytesIO(video_data)
                            st.video(video_file, format='video/mp4')

            if not found_letter_data:
                st.write("Data tidak ditemukan untuk huruf ini.")

            st.write("---")

    else:
        num_columns = 4  # Jumlah kolom yang diinginkan
        # Modified part for displaying videos for the input word
        st.header(f'Kata: {user_input}')

        output_folder = "kamusku"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        video_clips = []

        if user_input:
            alphabet_chunks = [user_input[i:i + num_columns] for i in range(0, len(user_input), num_columns)]
            image_number = 0
            for chunk in alphabet_chunks:
                columns = st.columns(len(chunk))
                for i, letter in enumerate(chunk):
                    image_number += 1
                    with columns[i]:
                        query = f"SELECT image_data FROM image_table WHERE id IN (SELECT image_data_id FROM kamus WHERE letter = %s);"
                        cursor.execute(query, (letter,))
                        result = cursor.fetchone()

                        if result:
                            image_data = result[0]
                            image = Image.open(io.BytesIO(image_data))
                            resized_image = resize_image(image, (200, 200))
                            st.image(resized_image, caption=f"{image_number}", width=150)

                    query = "SELECT video_data FROM video_table WHERE id IN (SELECT video_data_id FROM kamus WHERE letter = %s);"
                    cursor.execute(query, (letter,))
                    result = cursor.fetchone()

                    # If a video for the letter is found, save it as a file and add to video_clips list
                    if result:
                        video_data = result[0]
                        video_file_path = os.path.join(output_folder, f"{letter}.mp4")

                        # Save the video data as a file
                        with open(video_file_path, "wb") as video_file:
                            video_file.write(video_data)

                        # Add the video clip to the list
                        video_clip = VideoFileClip(video_file_path)
                        video_clips.append(video_clip)

    # Combine the video clips if any exist
            if video_clips:
                combined_clip = concatenate_videoclips(video_clips)
                combined_video_file = os.path.join(output_folder, "combined_video.mp4")
                combined_clip.write_videofile(combined_video_file, codec="libx264", audio_codec="aac")

                # Display the combined video using Streamlit
                st.video(combined_video_file, format='video/mp4')

                # Remove the individual video files
                for letter in user_input:
                    video_file_path = os.path.join(output_folder, f"{letter}.mp4")
                    if os.path.exists(video_file_path):
                        os.remove(video_file_path)
            else:
                st.write("Data tidak ditemukan untuk kata ini.")

                # Close the database connection
            connection.close()

if __name__ == '__main__':
    app()
