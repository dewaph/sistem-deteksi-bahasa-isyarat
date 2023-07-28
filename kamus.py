import streamlit as st
import mysql.connector

# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistem_deteksi_isyarat"
    )

# Function to check if image_data exists for the given letter in the image_table
def is_image_exists(letter):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT image_data_id FROM kamus WHERE letter=%s"
    cursor.execute(query, (letter,))
    result = cursor.fetchone()

    connection.close()

    return result[0] is not None if result else False

# Function to check if video_data exists for the given letter in the video_table
def is_video_exists(letter):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT video_data_id FROM kamus WHERE letter=%s"
    cursor.execute(query, (letter,))
    result = cursor.fetchone()

    connection.close()

    return result[0] is not None if result else False

# Function to save image and video data to the database and associate them with the kamus entry
def save_data_to_db(letter, image_data, video_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Save the image data to the image_table
    query = "INSERT INTO image_table (image_data) VALUES (%s)"
    cursor.execute(query, (image_data,))
    image_data_id = cursor.lastrowid

    # Save the video data to the video_table
    query = "INSERT INTO video_table (video_data) VALUES (%s)"
    cursor.execute(query, (video_data,))
    video_data_id = cursor.lastrowid

    # Save the image_data_id and video_data_id to the kamus table
    query = "INSERT INTO kamus (letter, image_data_id, video_data_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (letter, image_data_id, video_data_id))

    connection.commit()
    connection.close()

# Function to update image data in the image_table and associate it with the kamus entry
def update_data_in_db(letter, image_data, video_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if the letter exists in the kamus table
    query = "SELECT id, image_data_id, video_data_id FROM kamus WHERE letter=%s"
    cursor.execute(query, (letter,))
    result = cursor.fetchone()

    if result:
        kamus_id, existing_image_id, existing_video_id = result

        # Update the image data in the image_table
        query = "UPDATE image_table SET image_data=%s WHERE id=%s"
        cursor.execute(query, (image_data, existing_image_id))

        # Update the video data in the video_table
        query = "UPDATE video_table SET video_data=%s WHERE id=%s"
        cursor.execute(query, (video_data, existing_video_id))

    else:
        # If the letter does not exist, insert new data
        query = "INSERT INTO image_table (image_data) VALUES (%s)"
        cursor.execute(query, (image_data,))
        image_data_id = cursor.lastrowid

        query = "INSERT INTO video_table (video_data) VALUES (%s)"
        cursor.execute(query, (video_data,))
        video_data_id = cursor.lastrowid

        query = "INSERT INTO kamus (letter, image_data_id, video_data_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (letter, image_data_id, video_data_id))

    connection.commit()
    connection.close()

def delete_data_from_db(letter):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Get the data types (image and video) associated with the kamus entry
    query = "SELECT image_data_id, video_data_id FROM kamus WHERE letter=%s"
    cursor.execute(query, (letter,))
    result = cursor.fetchone()
    image_data_id, video_data_id = result if result else (None, None)

    if image_data_id is not None:
        # Delete the image data from the image_table
        query = "DELETE FROM image_table WHERE id=%s"
        cursor.execute(query, (image_data_id,))

    if video_data_id is not None:
        # Delete the video data from the video_table
        query = "DELETE FROM video_table WHERE id=%s"
        cursor.execute(query, (video_data_id,))

    # Remove the association in the kamus entry
    query = "UPDATE kamus SET image_data_id=NULL, video_data_id=NULL WHERE letter=%s"
    cursor.execute(query, (letter,))

    connection.commit()
    connection.close()

def get_data_from_db(letter, data_type):
    connection = get_db_connection()
    cursor = connection.cursor()

    if data_type == "image":
        query = "SELECT image_data FROM image_table WHERE id = (SELECT image_data_id FROM kamus WHERE letter = %s)"
    elif data_type == "video":
        query = "SELECT video_data FROM video_table WHERE id = (SELECT video_data_id FROM kamus WHERE letter = %s)"
    else:
        raise ValueError("Invalid data_type. Use 'image' or 'video'.")

    cursor.execute(query, (letter,))
    result = cursor.fetchone()

    connection.close()

    return result[0] if result else None



def app():
    st.title('Edit Kamus')

    alphabet_set = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    selected_letter = st.selectbox("Pilih Huruf", sorted(alphabet_set))

    st.write("---")

    st.header(f'Huruf {selected_letter}')

    col1, col2 = st.columns(2)

    with col1:
        uploaded_image = st.file_uploader(f'Unggah atau Edit gambar untuk huruf {selected_letter}', type=['png', 'jpg', 'jpeg'], key=f'upload_image_{selected_letter}')
        if uploaded_image is not None:
            image_data = uploaded_image.read()
            st.image(image_data, use_column_width=True)

    with col2:
        uploaded_video = st.file_uploader(f'Unggah atau Edit video untuk huruf {selected_letter}', type=['mp4'], key=f'upload_video_{selected_letter}')
        if uploaded_video is not None:
            video_data = uploaded_video.read()
            st.video(video_data)

    # Check if image and video exist in the database
    if is_image_exists(selected_letter) and is_video_exists(selected_letter):
        image_data = get_data_from_db(selected_letter, "image")
        if image_data:
            with col1:
                st.image(image_data, use_column_width=True)

        video_data = get_data_from_db(selected_letter, "video")
        if video_data:
            with col2:
                st.video(video_data)
        if col1.button("Simpan", key=f'save_or_edit_video_{selected_letter}'):
            if is_video_exists(selected_letter):
                update_data_in_db(selected_letter, image_data, video_data)
                st.success(
                    f"Data video untuk karakter {selected_letter} telah berhasil diperbarui di database.")
            else:
                save_data_to_db(selected_letter, image_data, video_data)
                st.success(f"Data video untuk karakter {selected_letter} telah berhasil disimpan ke database.")


    else:
        if uploaded_image and uploaded_video:
            if col1.button("Simpan", key=f'save_or_edit_video_{selected_letter}'):
                if is_video_exists(selected_letter):
                    update_data_in_db(selected_letter, image_data, video_data)
                    st.success(
                        f"Data video untuk karakter {selected_letter} telah berhasil diperbarui di database.")
                else:
                    save_data_to_db(selected_letter, image_data, video_data)
                    st.success(f"Data video untuk karakter {selected_letter} telah berhasil disimpan ke database.")

    # Create a new row for the "Hapus Gambar dan Video" button
    col3 = st.columns(1)
    with col3[0]:
        if st.button(f"Hapus Huruf {selected_letter} dari Database"):
            delete_data_from_db(selected_letter)
            st.success(f"Data gambar dan video untuk Huruf {selected_letter} telah berhasil dihapus dari database.")

if __name__ == '__main__':
    app()
