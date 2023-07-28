import mediapipe as mp
import numpy as np
import streamlit as st
import pickle
import cv2
import random
from streamlit_toggle import st_toggle_switch

def app():
    st.title('Praktek')
    st.header('Huruf Alfabet BISINDO')

    run_webcam_detection()


def run_webcam_detection():
    st.write("Tekan untuk menyalakan/mematikan kamera.")
    cols1, cols2, cols3, cols4 = st.columns([1, 1, 1, 1])
    with cols1:
        if 'button_clicked' not in st.session_state:
            st.session_state.button_clicked = False

        # Menambahkan tombol
        st.session_state.button_clicked = st_toggle_switch("Kamera", st.session_state.button_clicked)
        # if st_toggle_switch("Kamera"):
        #     st.session_state.button_clicked = not st.session_state.button_clicked

        # Menambahkan teks yang dapat berubah status diklik/non-diklik
    if st.session_state.button_clicked:
        st.markdown("Kamera <span style='background:#0cc958; border-radius: 2px;'>Aktif</span>", unsafe_allow_html=True)
        # Placeholder untuk menampilkan video
        placeholder = st.empty()

        # Inisialisasi webcam
        cap = cv2.VideoCapture(0)

        # Initialize the correct answer counter
        total_correct_answers = 0

        # Placeholder for displaying the total correct answers
        total_correct_placeholder = st.empty()
        run_detection(placeholder, cap, total_correct_answers, total_correct_placeholder)
    else:
        st.markdown("Kamera <span style='background:#c90c1f; border-radius: 2px;'>Mati</span>", unsafe_allow_html=True)

    # if camera_enabled:
    #     st.write("kamera menyala")


def run_detection(placeholder, cap, total_correct_answers, total_correct_placeholder):
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

    quiz_letter = random.choice(list(labels_dict1.values()) + list(labels_dict2.values()))
    quiz_answered = False
    previous_message = ""

    no_detection_time = 0  # Waktu tanpa deteksi

    while True:
        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()

        if not ret:
            break

        cv2.putText(frame, f'Praktekkan: Coba huruf {quiz_letter}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 0), 3, cv2.LINE_AA)

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

                # Initialize message with an empty string
                message = "Salah"

                if not quiz_answered:
                    prediction1 = model1.predict([np.asarray(data_aux)])
                    predicted_character = labels_dict1[int(prediction1[0])]

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                                cv2.LINE_AA)

                    if predicted_character == quiz_letter:
                        quiz_answered = True
                        cv2.putText(frame, "Isyarat Tangan Benar", (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                                    (0, 255, 0), 3, cv2.LINE_AA)
                        # Increment the total correct answers counter
                        total_correct_answers += 1

                    else:
                        message = "Masih Salah!"
                        message += "\nSilakan coba lagi."
                        cv2.putText(frame, "Isyarat Tangan Salah", (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                                    (0, 0, 255), 3, cv2.LINE_AA)

            else:
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10

                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                if not quiz_answered:
                    prediction2 = model2.predict([np.asarray(data_aux)])
                    predicted_character = labels_dict2[int(prediction2[0])]

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                                cv2.LINE_AA)

                    if predicted_character == quiz_letter:
                        quiz_answered = True
                        cv2.putText(frame, "Isyarat Tangan Benar", (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                                    (0, 255, 0), 3, cv2.LINE_AA)
                        # Increment the total correct answers counter
                        total_correct_answers += 1

                    else:
                        message = "Masih Salah!"
                        message += "\nSilakan coba lagi."
                        cv2.putText(frame, "Isyarat Tangan Salah", (x1, y1 - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                                    (0, 0, 255), 3, cv2.LINE_AA)

            if quiz_answered:
                # Generate new quiz
                quiz_letter = random.choice(list(labels_dict1.values()) + list(labels_dict2.values()))
                quiz_answered = False

            if message != previous_message:
                st.error(message)
                previous_message = message

        else:
            no_detection_time += 1  # Tambahkan waktu tanpa deteksi

            # Tampilkan pesan jika tidak ada deteksi selama 5 detik
            if no_detection_time == 50:
                st.warning("Tidak ada isyarat tangan yang terdeteksi. Arahkan tangan Anda ke dalam kamera.")

        # Tampilkan video yang diperbarui
        placeholder.image(frame, channels="BGR")

        # Update total correct answers in the fixed position placeholder
        total_correct_placeholder.text(f"Total Jawaban Benar: {total_correct_answers}")

    # Tutup webcam dan stop deteksi
    cap.release()
    cv2.destroyAllWindows()

app()
