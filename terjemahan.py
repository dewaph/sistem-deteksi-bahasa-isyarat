import mediapipe as mp
import numpy as np
import streamlit as st
import pickle
import cv2
import time
from gtts import gTTS
import pygame
import io

def speak_text(text):
    tts = gTTS(text=text, lang='id', slow=False)
    mp3_file = io.BytesIO()
    tts.write_to_fp(mp3_file)
    mp3_file.seek(0)

    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def app():
    st.subheader("Penerjemah Bahasa Isyarat Tangan Alfabet BISINDO")
    st.write("Klik tombol 'Buka Kamera' untuk memulai menerjemahkan Deteksi Bahasa Isyarat Huruf Alfabet BISINDO.")

    # Tombol untuk membuka webcam
    if st.button(':camera_with_flash: Buka Kamera'):
        st.write("INFO:")
        st.write("Tunggu beberapa detik untuk menerjemahkan isyarat tangan.")
        st.write("Jika diam tidak terdapat deteksi beberapa detik maka akan melakukan spasi untuk kata berikutnya.")
        # Placeholder untuk menampilkan video
        placeholder = st.empty()

        # Stop button
        stop_button = st.button(":x: Berhenti")

        # Inisialisasi webcam
        cap = cv2.VideoCapture(0)

        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles

        hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)

        model_dict1 = pickle.load(open('./machinelearning/model/model1.p', 'rb'))
        model_dict2 = pickle.load(open('./machinelearning/model/model2.p', 'rb'))
        model1 = model_dict1['model1']
        model2 = model_dict2['model2']

        labels_dict1 = {0: 'C', 1: 'E', 2: 'I', 3: 'J', 4: 'L', 5: 'O', 6: 'R', 7: 'U', 8: 'V', 9: 'Z'}
        labels_dict2 = {0: 'A', 1: 'B', 2: 'D', 3: 'F', 4: 'G', 5: 'H', 6: 'K', 7: 'M', 8: 'N', 9: 'P',
                        10: 'Q', 11: 'S', 12: 'T', 13: 'W', 14: 'X', 15: 'Y'}

        transcript = ""
        start_time = None  # Waktu awal deteksi
        no_detection_time = 0  # Waktu tanpa deteksi

        # Placeholder untuk menampilkan transkrip
        transkrip_placeholder = st.empty()

        while True:
            data_aux = []
            x_ = []
            y_ = []

            ret, frame = cap.read()

            if not ret:
                break

            cv2.putText(frame, 'Mulai Menerjemahkan', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                        cv2.LINE_AA)

            H, W, _ = frame.shape

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                no_detection_time = 0  # Reset waktu tanpa deteksi
                n = len(results.multi_hand_landmarks)
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,  # image to draw
                        hand_landmarks,  # model output
                        mp_hands.HAND_CONNECTIONS,  # hand connections
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

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

                if n == 1:
                    x1 = int(min(x_) * W) - 10
                    y1 = int(min(y_) * H) - 10

                    x2 = int(max(x_) * W) - 10
                    y2 = int(max(y_) * H) - 10

                    if start_time is None:
                        start_time = time.time()  # Set waktu awal jika belum diinisialisasi

                    if start_time is not None and time.time() - start_time >= 1.5:
                        prediction1 = model1.predict([np.asarray(data_aux)])
                        predicted_character = labels_dict1[int(prediction1[0])]


                        # Tambahkan hasil prediksi huruf selanjutnya
                        if predicted_character != ' ' or transcript[-1] != ' ':
                            transcript += predicted_character + " "
                            speak_text(predicted_character)

                        start_time = None  # Reset waktu awal

                else:
                    x1 = int(min(x_) * W) - 10
                    y1 = int(min(y_) * H) - 10

                    x2 = int(max(x_) * W) - 10
                    y2 = int(max(y_) * H) - 10

                    if start_time is None:
                        start_time = time.time()  # Set waktu awal jika belum diinisialisasi

                    if start_time is not None and time.time() - start_time >= 1.5:
                        prediction2 = model2.predict([np.asarray(data_aux)])
                        predicted_character = labels_dict2[int(prediction2[0])]


                        # Tambahkan hasil prediksi huruf selanjutnya
                        if predicted_character != ' ' or transcript[-1] != ' ':
                            transcript += predicted_character + " "
                            speak_text(predicted_character)

                        start_time = None  # Reset waktu awal

                # Tampilkan transkrip
                transkrip_placeholder.text("Terjemahan: " + transcript)

            # Tampilkan frame pada placeholder
            placeholder.image(frame, channels="BGR")

            if stop_button:
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app()