import pandas as pd
import streamlit as st
import mysql.connector



# st.set_page_config(layout='wide', initial_sidebar_state='expanded')
# Fungsi untuk menghubungkan ke database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sistem_deteksi_isyarat"
    )

def count_data_in_table(table_name):
    # Fungsi ini akan menghitung jumlah data di dalam suatu tabel di database
    connection = get_db_connection()
    cursor = connection.cursor()

    query = f"SELECT COUNT(*) FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchone()[0]

    connection.close()

    return result

def count_unique_labels(table_name):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = f"SELECT class_label, huruf, COUNT(*) AS count FROM {table_name} GROUP BY class_label"
    cursor.execute(query)
    result = cursor.fetchall()

    connection.close()

    return result

# Fungsi untuk menghapus data berdasarkan huruf
def delete_data_by_huruf(table_name, huruf):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = f"DELETE FROM {table_name} WHERE huruf = %s"
    cursor.execute(query, (huruf,))
    connection.commit()

    connection.close()

# Fungsi untuk memperbarui data berdasarkan huruf
def edit_data_by_huruf(table_name, huruf, new_huruf):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = f"UPDATE {table_name} SET huruf = %s WHERE huruf = %s"

    cursor.execute(query, (new_huruf, huruf))
    connection.commit()

    connection.close()

def edit_label_by_huruf(table_name, huruf, new_label):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = f"UPDATE {table_name} SET class_label = %s WHERE huruf = %s"

    cursor.execute(query, (new_label, huruf))
    connection.commit()

    connection.close()

with open('style\style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def app():
    # Hitung jumlah data di tabel data_1_tangan
    data1tangan_count = count_data_in_table('data_1_tangan')

    # Hitung jumlah data di tabel data_2_tangan
    data2tangan_count = count_data_in_table('data_2_tangan')

    # Jumlahkan jumlah data dari data_1_tangan dan data_2_tangan
    total_data_count = data1tangan_count + data2tangan_count

    # Row A
    st.markdown('### Dashboard')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Data", total_data_count)
    col2.metric("Data 1 tangan", data1tangan_count)
    col3.metric("Data 2 tangan", data2tangan_count)

    # Count unique class labels in data_1_tangan and data_2_tangan
    unique_labels_data1 = count_unique_labels('data_1_tangan')
    unique_labels_data2 = count_unique_labels('data_2_tangan')

    col4.metric("Jumlah Label", len((unique_labels_data1 + unique_labels_data2)))
    st.write("---")

    # Data Tables
    col5, col6 = st.columns(2)
    col5.subheader("Tabel Data 1 Tangan")
    data1_df = pd.DataFrame(unique_labels_data1, columns=['label','huruf', 'jumlah'])
    col5.dataframe(data1_df, width=600, hide_index = True)  # Increase width to 600

    col6.subheader("Tabel Data 2 Tangan")
    data2_df = pd.DataFrame(unique_labels_data2, columns=['label','huruf', 'jumlah'])
    col6.dataframe(data2_df, width=600, hide_index = True)  # Increase width to 600


    # Selectbox to choose between "data_1_tangan" and "data_2_tangan"
    selected_table = st.selectbox("Pilih Data:", ["data_1_tangan", "data_2_tangan"])

    # Display Class Labels and Counts
    if selected_table == "data_1_tangan":

        # Delete and Edit functionality for data_1_tangan
        action_selectbox = st.selectbox("Action (Data 1)", ["Delete Data", "Edit Data"])
        selected_huruf = st.selectbox("Pilih Huruf", data1_df['huruf'].unique())

        if action_selectbox == "Delete Data":
            if st.button("Delete Data"):
                delete_data_by_huruf('data_1_tangan', selected_huruf)
                st.success(f"Data Huruf {selected_huruf} dihapus")
        elif action_selectbox == "Edit Data":
            edit_action = st.selectbox("Pilih Edit (Data 1)", ["Edit Huruf", "Edit Label"])
            current_data = data1_df[data1_df['huruf'] == selected_huruf]

            if not current_data.empty:
                current_data = current_data.iloc[0]
                st.write("Data Saat ini (Data 1):")
                st.write(current_data)

                if edit_action == "Edit Huruf":
                    # Input field for editing huruf (data_1_tangan)
                    new_huruf = st.text_input("Masukkan Huruf Baru (Data 1)", selected_huruf).upper()
                    if st.button("Edit Huruf"):
                        edit_data_by_huruf('data_1_tangan', selected_huruf, new_huruf)
                        st.success(
                            f"Data Huruf {selected_huruf} berhasil diubah ke huruf {new_huruf}")

                elif edit_action == "Edit Label":
                    # Input field for editing label (data_1_tangan)
                    new_label = st.text_input("Masukkan Label Baru (Data 1)", current_data['label'])
                    if st.button("Edit Label"):
                        edit_label_by_huruf('data_1_tangan', selected_huruf, new_label)
                        st.success(
                            f"Label Huruf {selected_huruf} berhasil diubah ke label {new_label}")
            else:
                st.warning(f"No data found for Huruf {selected_huruf} in data_1_tangan.")

    elif selected_table == "data_2_tangan":

        # Delete and Edit functionality for data_2_tangan
        action_selectbox = st.selectbox("Pilih (Data 2)", ["Delete Data", "Edit Data"])
        selected_huruf = st.selectbox("Pilih Huruf (Data 2)", data2_df['huruf'].unique())

        if action_selectbox == "Delete Data":
            if st.button("Delete Data (Data 2)"):
                delete_data_by_huruf('data_2_tangan', selected_huruf)
                st.success(f"Data Huruf {selected_huruf} dihapus")
        elif action_selectbox == "Edit Data":
            edit_action = st.selectbox("Select Action (Data 2)", ["Edit Huruf", "Edit Label"])
            current_data = data2_df[data2_df['huruf'] == selected_huruf]

            if not current_data.empty:
                current_data = current_data.iloc[0]
                st.write("Current Data (Data 2):")
                st.write(current_data)

                if edit_action == "Edit Huruf":
                    # Input field for editing huruf (data_2_tangan)
                    new_huruf = st.text_input("Enter New Huruf (Data 2)", selected_huruf).upper()
                    if st.button("Edit Huruf (Data 2)"):
                        edit_data_by_huruf('data_2_tangan', selected_huruf, new_huruf)
                        st.success(
                            f"Data Huruf {selected_huruf} berhasil diubah ke huruf {new_huruf}")

                elif edit_action == "Edit Label":
                    # Input field for editing label (data_2_tangan)
                    new_label = st.text_input("Enter New Label (Data 2)", current_data['label'])
                    if st.button("Edit Label (Data 2)"):
                        edit_label_by_huruf('data_2_tangan', selected_huruf, new_label)
                        st.success(
                            f"Label Huruf {selected_huruf} berhasil diubah ke label {new_label}")
            else:
                st.warning(f"No data found for Huruf {selected_huruf} in data_2_tangan.")


if __name__ == '__main__':
    app()
