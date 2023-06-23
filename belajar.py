import streamlit as st
from PIL import Image
def app():
    st.title('Belajar Huruf Alfabet Isyarat')

    st.header('BISINDO')
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def resize_image(image_path, size):
        image = Image.open(image_path)
        resized_image = image.resize(size)
        return resized_image

    num_columns = 4  # Jumlah kolom yang diinginkan
    alphabet_chunks = [alphabet[i:i+num_columns] for i in range(0, len(alphabet), num_columns)]
    for chunk in alphabet_chunks:
        column = st.columns(len(chunk))
        for i, letter in enumerate(chunk):
            image_path = f'images/{letter}.png'  # Ganti dengan PATH gambar yang sesuai untuk masing-masing huruf
            resized_image = resize_image(image_path, (200, 200))  # Ganti ukuran sesuai kebutuhan Anda
            column[i].image(resized_image, width=150)

        button_column = st.columns(len(chunk))
        for i, letter in enumerate(chunk):
            if button_column[i].button(f'VIDEO "{letter}"'):  # Menambahkan tombol dengan teks sesuai huruf
                video_path = f'videos/{letter}.mp4'  # Ganti dengan PATH video yang sesuai untuk masing-masing huruf
                st.video(video_path)
        st.markdown("""
        <style>
        div.stButton > button:first-child {
        font-family: Hack, monospace;
        background: #C41F1E;
        color: white;
        cursor: pointer;
        font-size: 2em;
        padding: 1rem;
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

if __name__ == '__main__':
    app()
