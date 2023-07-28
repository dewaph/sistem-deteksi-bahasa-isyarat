import streamlit as st
import cv2
import csv
import mediapipe as mp
import numpy as np
import mysql.connector
import os


# Function to connect to the database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistem_deteksi_isyarat"
    )


# Function to get images from the database based on class_label
def get_images_from_db(class_label, num_images=5, dataset=1):
    if dataset == 1:
        table_name = "data_1_tangan"
    elif dataset == 2:
        table_name = "data_2_tangan"
    else:
        return None

    connection = get_db_connection()
    cursor = connection.cursor()

    query = f"SELECT image_data FROM {table_name} WHERE class_label = %s LIMIT %s"
    cursor.execute(query, (class_label, num_images))
    images_data = cursor.fetchall()

    connection.close()

    return images_data


label_dataset_1 = {
    0: 'C',
    1: 'E',
    2: 'I',
    3: 'J',
    4: 'L',
    5: 'O',
    6: 'R',
    7: 'U',
    8: 'V',
    9: 'Z'
}

label_dataset_2 = {
    0: 'A',
    1: 'B',
    2: 'D',
    3: 'F',
    4: 'G',
    5: 'H',
    6: 'K',
    7: 'M',
    8: 'N',
    9: 'P',
    10: 'Q',
    11: 'S',
    12: 'T',
    13: 'W',
    14: 'X',
    15: 'Y'
}

# Function to fetch image data from the "data_1_tangan" table in the database
def fetch_data_from_db1():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT class_label, image_data FROM data_1_tangan"
    cursor.execute(query)
    result = cursor.fetchall()

    connection.close()

    return result

def fetch_data_from_db2():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT class_label, image_data FROM data_2_tangan"
    cursor.execute(query)
    result = cursor.fetchall()

    connection.close()

    return result


def process_hand_landmarks_data1():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.3)

    # Fetch image data from the database
    data_from_db = fetch_data_from_db1()

    data = []
    labels = []
    for class_label, image_data in data_from_db:
        data_aux = []

        x_ = []
        y_ = []

        # Convert image data from bytes to numpy array
        image_np = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)

        if not (results.multi_hand_landmarks is None):
            n = len(results.multi_hand_landmarks)
            if n == 1:
                try:
                    for hand_landmarks in results.multi_hand_landmarks:
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            x_.append(x)
                            y_.append(y)
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            data_aux.append(x - min(x_))
                            data_aux.append(y - min(y_))
                    data.append(data_aux)
                    labels.append(class_label)
                except:
                    data_aux = np.zeros([1, 63], dtype=np.float32)[0]

    if len(data) > 0 and len(labels) > 0:
        folder_path = "download"
        csv_filename = "onehand.csv"
        file_path = os.path.join(folder_path, csv_filename)
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['label'] + [f'data_{i}' for i in range(len(data[0]))])  # Writing column headers

            for i in range(len(data)):
                label = labels[i]
                data_row = np.asarray(data[i], dtype=np.float32)
                writer.writerow([label] + data_row.tolist())

        st.success("CSV file for hand landmarks data successfully created.")  # CSV successfully created
        return file_path
    else:
        st.warning("No data collected, unable to create CSV.")  # No data collected, unable to create CSV
        return None

def process_hand_landmarks_data2():
    mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)

    # Fetch image data and class labels from the database
    data_from_db = fetch_data_from_db2()

    data = []
    labels = []
    for class_label, image_data in data_from_db:
        data_aux = []

        x_ = []
        y_ = []

        # Convert image data from bytes to numpy array
        image_np = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = mp_hands.process(img_rgb)

        if not (results.multi_hand_landmarks is None):
            n = len(results.multi_hand_landmarks)
            if n == 2:
                try:
                    for hand_landmarks in results.multi_hand_landmarks:
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            x_.append(x)
                            y_.append(y)
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            data_aux.append(x - min(x_))
                            data_aux.append(y - min(y_))
                    data.append(data_aux)
                    labels.append(class_label)
                except:
                    data_aux = np.zeros([1, 189], dtype=np.float32)[0]

    if len(data) > 0 and len(labels) > 0:
        folder_path = "download"
        csv_filename = "twohand.csv"
        file_path = os.path.join(folder_path, csv_filename)
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['label'] + [f'data_{i}' for i in range(len(data[0]))])  # Writing column headers

            for i in range(len(data)):
                label = labels[i]
                data_row = np.asarray(data[i], dtype=np.float32)
                writer.writerow([label] + data_row.tolist())

        st.success("CSV file for hand landmarks data successfully created.")  # CSV successfully created
        return file_path
    else:
        st.warning("No data collected, unable to create CSV.")  # No data collected, unable to create CSV
        return None
# Function to process and display images
def process_images(dataset):
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)

    if dataset == 1:
        label = label_dataset_1
    elif dataset == 2:
        label = label_dataset_2
    else:
        return None

    # Create Streamlit app
    st.title(f'Gambar untuk data tangan (Dataset {dataset})')
    number_of_classes = len(label)
    num_images_to_display = 5

    for j in range(number_of_classes):
        st.header(f"Menampilkan gambar untuk kelas {label[j]}")

        # Get images from the database for the current class
        images_data = get_images_from_db(j, num_images=num_images_to_display, dataset=dataset)

        # Create a Streamlit layout for displaying images
        col_images = st.columns(num_images_to_display)

        for i, image_data in enumerate(images_data):
            # Convert image_data (bytes) to numpy array for OpenCV
            nparr = np.frombuffer(image_data[0], np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Convert BGR to RGB for MediaPipe Hands
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Process hand landmarks using MediaPipe Hands
            results = mp_hands.process(img_rgb)

            # Display the image with hand landmarks (if detected) on the corresponding column
            with col_images[i]:
                st.image(img_rgb, use_column_width=True, channels='RGB', caption=f"Gambar {i + 1}")

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp.solutions.drawing_utils.draw_landmarks(
                            img_rgb,
                            hand_landmarks,
                            mp.solutions.hands.HAND_CONNECTIONS,
                            mp.solutions.drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                            mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)
                        )

                    st.image(img_rgb, use_column_width=True, channels='RGB',
                             caption=f"Gambar {i + 1} with hand landmarks")

            st.write("")  # Add an empty line between images

    # Close MediaPipe Hands
    mp_hands.close()


# Create Streamlit app
def app():
    st.title("Preprocessing Data")
    st.write("Klik tombol dibawah untuk memulai preprocessing gambar.")

    if st.button("PreProcess Images"):
        process_images(dataset=1)
        process_images(dataset=2)

    if st.button("Download CSV data 1 tangan"):
        # Process the hand landmarks data and get the CSV filename
        process_hand_landmarks_data1()

    if st.button("Download CSV data 2 tangan"):
        # Process the hand landmarks data and get the CSV filename
        process_hand_landmarks_data2()

if __name__ == "__main__":
    app()
