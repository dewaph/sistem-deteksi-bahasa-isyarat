import streamlit as st
import mysql.connector
import cv2
import numpy as np

# Function to get database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistem_deteksi_isyarat"
    )

# Function to check if the specified table is empty
def is_table_empty(table_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchone()[0]

    connection.close()

    return result == 0

# Function to resize the image using OpenCV
def resize_and_save_image(image_data, max_size=(256, 256)):
    try:
        # Convert the image data to a NumPy array
        np_array = np.frombuffer(image_data, np.uint8)
        image_np = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        # Resize the image while maintaining the aspect ratio
        height, width = image_np.shape[:2]
        ratio = min(max_size[0] / width, max_size[1] / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        resized_image = cv2.resize(image_np, (new_width, new_height), interpolation=cv2.INTER_AREA)

        # Encode the resized image to bytes
        _, image_data_resized = cv2.imencode(".jpg", resized_image)
        image_data_resized_bytes = image_data_resized.tobytes()

        return image_data_resized_bytes

    except Exception as e:
        print(f"Error during image resizing: {e}")
        return None

# Function to save the uploaded photo to the specified table in the database
def save_photo_to_db(image_data, huruf, table_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if the huruf already exists in the database
    query = f"SELECT class_label FROM {table_name} WHERE huruf = %s"
    cursor.execute(query, (huruf,))
    result = cursor.fetchall()

    if result:
        # If huruf exists, use the existing class_label
        class_label = result[0][0]
    else:
        # If huruf does not exist, create a new class_label
        query = f"SELECT MAX(class_label) FROM {table_name}"
        cursor.execute(query)
        max_class_label = cursor.fetchone()[0]
        class_label = max_class_label + 1 if max_class_label is not None else 0

    # Save the image data to the table in the database
    query = f"INSERT INTO {table_name} (class_label, image_data, huruf) VALUES (%s, %s, %s)"
    cursor.execute(query, (class_label, image_data, huruf))

    connection.commit()
    connection.close()

# Streamlit app
def app():
    st.title("Tambah Dataset")

    table_options = ["data_1_tangan", "data_2_tangan"]
    selected_table = st.selectbox("Pilih tabel untuk mengunggah foto:", table_options)

    # Check if the selected table is empty
    data_table_empty = is_table_empty(selected_table)

    # If the table is empty, allow the user to upload huruf and gambar
    if data_table_empty:
        huruf = st.text_input("Masukkan huruf baru:").upper()
        uploaded_files = st.file_uploader("Pilih foto", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

        # Add a button to trigger the photo upload to the selected table in the database
        if uploaded_files and huruf:
            if st.button("Tambah Data"):
                for uploaded_file in uploaded_files:
                    try:
                        # Read the image using OpenCV
                        image_data = uploaded_file.read()

                        # Resize the image using OpenCV before saving to the database
                        image_data_resized = resize_and_save_image(image_data)

                        if image_data_resized is not None:
                            # Save the resized image data to the selected table in the database
                            save_photo_to_db(image_data_resized, huruf, selected_table)
                        else:
                            st.error("Error occurred during image resizing. Please upload a valid image.")

                    except Exception as e:
                        st.error(f"Error processing the uploaded image: {e}")

                st.success("Foto-foto berhasil ditambahkan ke database.")

    # If the table is not empty, allow the user to select huruf or add new huruf
    else:
        st.subheader(f"Pilih atau tambahkan huruf untuk {selected_table}:")
        connection = get_db_connection()
        cursor = connection.cursor()
        query = f"SELECT DISTINCT huruf FROM {selected_table}"
        cursor.execute(query)
        existing_huruf_choices = [row[0] for row in cursor.fetchall()]
        connection.close()

        huruf = st.selectbox("Pilih huruf:", existing_huruf_choices + ["Tambah huruf baru"])

        # If user selects "Tambah huruf baru", allow them to input the new huruf
        if huruf == "Tambah huruf baru":
            huruf = st.text_input("Masukkan huruf baru:").upper()
            if huruf:
                uploaded_files = st.file_uploader("Pilih foto", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

                # Add a button to trigger the photo upload to the selected table in the database
                if uploaded_files:
                    if st.button("Tambah Data"):
                        for uploaded_file in uploaded_files:
                            try:
                                # Read the image using OpenCV
                                image_data = uploaded_file.read()

                                # Resize the image using OpenCV before saving to the database
                                image_data_resized = resize_and_save_image(image_data)

                                if image_data_resized is not None:
                                    # Save the resized image data to the selected table in the database
                                    save_photo_to_db(image_data_resized, huruf, selected_table)
                                else:
                                    st.error("Error occurred during image resizing. Please upload a valid image.")

                            except Exception as e:
                                st.error(f"Error processing the uploaded image: {e}")

                        st.success(f"Foto-foto berhasil diunggah ke database dengan huruf {huruf}.")

        # If user selects an existing huruf, proceed with photo upload
        elif huruf in existing_huruf_choices:
            uploaded_files = st.file_uploader("Pilih foto", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

            # Add a button to trigger the photo upload to the selected table in the database
            if uploaded_files:
                if st.button("Tambah Data"):
                    for uploaded_file in uploaded_files:
                        try:
                            # Read the image using OpenCV
                            image_data = uploaded_file.read()

                            # Resize the image using OpenCV before saving to the database
                            image_data_resized = resize_and_save_image(image_data)

                            if image_data_resized is not None:
                                # Save the resized image data to the selected table in the database
                                save_photo_to_db(image_data_resized, huruf, selected_table)
                            else:
                                st.error("Error occurred during image resizing. Please upload a valid image.")

                        except Exception as e:
                            st.error(f"Error processing the uploaded image: {e}")

                    st.success(f"Foto-foto berhasil diunggah ke database dengan huruf {huruf}.")

if __name__ == "__main__":
    app()
