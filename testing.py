import streamlit as st
import cv2
import mediapipe as mp
import pickle
import numpy as np

model_dict1 = pickle.load(open('./machinelearning/model/model1.p', 'rb'))
model_dict2 = pickle.load(open('./machinelearning/model/model2.p', 'rb'))
model1 = model_dict1['model1']
model2 = model_dict2['model2']

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

labels_dict1 = {0: 'C', 1: 'E', 2: 'I', 3: 'J', 4: 'L', 5: 'O', 6: 'R', 7: 'U', 8: 'V', 9: 'Z', 16: ''}
labels_dict2 = {0: 'A', 1: 'B', 2: 'D', 3: 'F', 4: 'G', 5: 'H', 6: 'K', 7: 'M', 8: 'N', 9: 'P',
                10: 'Q', 11: 'S', 12: 'T', 13: 'W', 14: 'X', 15: 'Y', 16: ''}


def predict_character(data_aux, model, labels_dict):
    prediction = model.predict([np.asarray(data_aux)])
    return labels_dict[int(prediction[0])]


def app():
    st.title("Real Time Testing")

    # Add a button to start the camera
    start_button = st.button("Start Camera")

    if start_button:

        # Create a placeholder for the camera feed
        video_placeholder = st.empty()

        cap = cv2.VideoCapture(0)

        hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.3)

        # Display the "Stop Camera" button when the "Start Camera" button is clicked
        stop_button = st.button("Stop Camera")

        while start_button:
            ret, frame = cap.read()

            H, W, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                data_aux = []
                x_ = []
                y_ = []

                n = len(results.multi_hand_landmarks)
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,  # image to draw
                        hand_landmarks,  # model output
                        mp_hands.HAND_CONNECTIONS,  # hand connections
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

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

                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10

                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                if n == 1:
                    predicted_character = predict_character(data_aux, model1, labels_dict1)
                else:
                    predicted_character = predict_character(data_aux, model2, labels_dict2)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                            cv2.LINE_AA)

            video_placeholder.image(frame, channels="BGR")

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app()