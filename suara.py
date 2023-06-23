import streamlit as st
import speech_recognition as sr

def app():
    st.subheader("Deteksi Suara")
    st.write("Klik tombol 'Rekam Suara' untuk memulai berbicara dan Suara akan diterjemahkan ke dalam Teks.")

    # Tombol untuk memulai dan menghentikan pengenalan suara
    if st.button(':studio_microphone: Rekam Suara'):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.markdown("<p style='color: red;'>Mulai berbicara...</p>", unsafe_allow_html=True)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language='id-ID')
            st.write("Terjemahan:")
            st.success(text)
        except sr.UnknownValueError:
            st.write("Tidak dapat mengenali suara")
        except sr.RequestError as e:
            st.write("Terjadi kesalahan pada layanan pengenalan suara:", str(e))


if __name__ == '__main__':
    app()