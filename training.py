import streamlit as st
import pandas as pd
import csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report,confusion_matrix
import seaborn as sns
import pickle
import os

st.set_option('deprecation.showPyplotGlobalUse', False)

# Create folders to store uploaded CSV files
SAVE_DIR1 = "machinelearning/data1tangan"
SAVE_DIR2 = "machinelearning/data2tangan"
os.makedirs(SAVE_DIR1, exist_ok=True)
os.makedirs(SAVE_DIR2, exist_ok=True)

def save_csv_file(file, save_dir):
    if file is not None:
        filepath = os.path.join(save_dir, file.name)
        with open(filepath, "wb") as f:
            f.write(file.getbuffer())
        return filepath
    return None

# Function to load data from CSV
def load_data_from_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        data = list(reader)
        df = pd.DataFrame(data, columns=headers)
        x = df.drop('label', axis=1)
        y = df['label']
    return x, y

def app():
    st.title("Training Model")

    # File upload for data1tangan
    st.subheader("Data 1 Tangan")
    uploaded_file1 = st.file_uploader("Upload a CSV file", type=["csv"], key="data1tangan")

    if uploaded_file1 is not None:
        # Display the uploaded file
        st.subheader("Uploaded CSV file for Data 1 Tangan:")
        st.write(uploaded_file1)

        # Save the uploaded file locally
        save_path1 = save_csv_file(uploaded_file1, SAVE_DIR1)

        if save_path1:
            st.success(f"File saved successfully at {save_path1}")
        else:
            st.error("Failed to save the file.")

        # Display the contents of the uploaded CSV file for Data 1 Tangan
        st.subheader("Contents of the uploaded CSV file:")
        df1 = pd.read_csv(uploaded_file1)
        st.dataframe(df1)

    # File upload for data2tangan
    st.subheader("Data 2 Tangan")
    uploaded_file2 = st.file_uploader("Upload a CSV file", type=["csv"], key="data2tangan")

    if uploaded_file2 is not None:
        # Display the uploaded file
        st.subheader("Uploaded CSV file for Data 2 Tangan:")
        st.write(uploaded_file2)

        # Save the uploaded file locally
        save_path2 = save_csv_file(uploaded_file2, SAVE_DIR2)

        if save_path2:
            st.success(f"File saved successfully at {save_path2}")
        else:
            st.error("Failed to save the file.")

        # Display the contents of the uploaded CSV file for Data 2 Tangan
        st.subheader("Contents of the uploaded CSV file:")
        df2 = pd.read_csv(uploaded_file2)
        st.dataframe(df2)

        # Add a button to start processing
    if st.button("Start Processing"):
        # Load data from onehand.csv
        x, y = load_data_from_csv('./machinelearning/data1tangan/onehand.csv')

        # Load data from twohand.csv
        x2, y2 = load_data_from_csv('./machinelearning/data2tangan/twohand.csv')

        # Split data into training and test sets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=True, stratify=y)
        x_train2, x_test2, y_train2, y_test2 = train_test_split(x2, y2, test_size=0.2, shuffle=True, stratify=y2)

        # Train models
        model1 = RandomForestClassifier()
        model2 = RandomForestClassifier()

        model1.fit(x_train, y_train)
        model2.fit(x_train2, y_train2)

        # Make predictions on test data
        y_predict = model1.predict(x_test)
        y_predict2 = model2.predict(x_test2)

        # Calculate accuracy scores
        score1 = accuracy_score(y_test, y_predict)
        score2 = accuracy_score(y_test2, y_predict2)

        # Calculate precision, recall, and F1-score
        report1 = classification_report(y_test, y_predict)
        report2 = classification_report(y_test2, y_predict2)

        # Display accuracy scores
        st.subheader("Model 1 (Data 1 Tangan)")
        st.write(f"Accuracy: {score1 * 100:.2f}%")
        st.write("Classification Report:")
        st.text(report1)
        # Plot confusion matrix for model1
        label1 = {'C': 0, 'E': 1, 'I': 2, 'J': 3, 'L': 4, 'O': 5, 'R': 6, 'U': 7, 'V': 8, 'Z': 9
                  }

        label2 = {'A': 0, 'B': 1, 'D': 2, 'F': 3, 'G': 4, 'H': 5, 'K': 6, 'M': 7, 'N': 8, 'P': 9, 'Q': 10,
                  'S': 11, 'T': 12, 'W': 13, 'X': 14, 'Y': 15
                  }
        labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']

        # Plot confusion matrix for model1
        cm1 = confusion_matrix(y_test, y_predict)
        st.subheader("Confusion Matrix - Model 1")
        sns.heatmap(cm1, annot=True, fmt='d', cmap='Blues',
                    xticklabels=label1, yticklabels=label1)
        st.pyplot()

        st.subheader("Model 2 (Data 2 Tangan)")
        st.write(f"Accuracy: {score2 * 100:.2f}%")
        st.write("Classification Report:")
        st.text(report2)
        # Plot confusion matrix for model1
        cm2 = confusion_matrix(y_test2, y_predict2)
        st.subheader("Confusion Matrix - Model 1")
        sns.heatmap(cm2, annot=True, fmt='d', cmap='Blues',
                    xticklabels=label2, yticklabels=label2)
        st.pyplot()

        # Save models as pickle files
        model1_filename = os.path.join('./machinelearning/model', 'model1.p')
        os.makedirs(os.path.dirname(model1_filename), exist_ok=True)
        with open(model1_filename, 'wb') as f:
            pickle.dump({'model1': model1}, f)

        model2_filename = os.path.join('./machinelearning/model', 'model2.p')
        os.makedirs(os.path.dirname(model2_filename), exist_ok=True)
        with open(model2_filename, 'wb') as f:
            pickle.dump({'model2': model2}, f)

        st.success("Models have been saved to 'machinelearning/model' folder.")

if __name__ == "__main__":
    app()
