import streamlit as st
import mysql.connector
import subprocess
import os
# Koneksi ke database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sistem_deteksi_isyarat"
)

def is_username_taken(username):
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

def register(username, password):
    if not username or not password:
        st.error("Username dan password tidak boleh kosong.")
        return

    if is_username_taken(username):
        return

    cursor = db.cursor()
    query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    # Set role sebagai 'user' saat mendaftar
    cursor.execute(query, (username, password, 'user'))
    db.commit()
    cursor.close()

# Fungsi untuk memeriksa login
def login(username, password):
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username=%s AND password=%s AND role=%s"
    cursor.execute(query, (username, password, 'admin'))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return 'admin'  # Mengembalikan nilai 'admin' jika login berhasil
    else:
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username=%s AND password=%s AND role=%s"
        cursor.execute(query, (username, password, 'user'))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return 'user'  # Mengembalikan nilai 'user' jika login berhasil
        else:
            return None  # Mengembalikan None jika login gagal

# Halaman Login
def login_page():
    # Menggunakan layout grid untuk mengatur tata letak elemen di tengah halaman
    col1, col2, col3 = st.columns(3)
    col1.write("")  # Kolom kosong untuk ruang kosong di sebelah kiri
    col2.write("")  # Kolom kosong untuk ruang kosong di sebelah kanan
    with col2:

        # Menampilkan judul "Login" di tengah halaman
        st.title("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            if not username or not password:
                st.error("Username dan password tidak boleh kosong.")
            else:
                if register(username, password):
                    st.success("Pendaftaran berhasil!")
                else:
                    st.error("Username sudah ada. Pendaftaran gagal.")

        if st.button("Login"):
            if not username or not password:
                st.error("Username dan password harus diisi.")
            else:
                role = login(username, password)
                if role:
                    st.success("Login berhasil!")
                    if role == "admin":
                        # Mengarahkan pengguna ke halaman admin
                        subprocess.Popen(["streamlit", "run", "admin.py"])
                        os._exit(0)  # Menutup index.py

                    elif role == "user":
                        # Mengarahkan pengguna ke halaman main.py
                        subprocess.Popen(["streamlit", "run", "main.py"])
                        os._exit(0)  # Menutup index.py

                else:
                    st.error("Username atau password salah.")

if __name__ == "__main__":
    login_page()