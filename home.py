import streamlit as st
import requests
from streamlit_lottie import st_lottie


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://lottie.host/160d083e-a377-4a60-b5af-3310a3544375/zemzhLgni6.json")
hello = load_lottieurl("https://lottie.host/aff1e6dc-1cb7-4979-8616-0ee5b8540c1b/SunicAdA8Q.json")

def app():
    st.markdown("""
            <style>
            div.stButton > button:first-child {
            width: 220px;
            height: 50px;
            border: none;
            outline: none;
            color: #fff;
            background: #111;
            cursor: pointer;
            position: relative;
            z-index: 0;
            border-radius: 10px;
            
            &:before {
    content: '';
    background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
    position: absolute;
    top: -2px;
    left:-2px;
    background-size: 400%;
    z-index: -1;
    filter: blur(5px);
    width: calc(100% + 4px);
    height: calc(100% + 4px);
    animation: glowing 20s linear infinite;
    opacity: 0;
    transition: opacity .3s ease-in-out;
    border-radius: 10px;
}
&:active {
    color: #000
}
&:active:after {
    background: transparent;
}
&:hover:before {
    opacity: 1;
}
&:after {
    z-index: -1;
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: #111;
    left: 0;
    top: 0;
    border-radius: 10px;
}}
@keyframes glowing {
    0% { background-position: 0 0; }
    50% { background-position: 400% 0; }
    100% { background-position: 0 0; }
}
            </style>""", unsafe_allow_html=True)
    # ---- HEADER SECTION ----
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader("Selamat Datang :wave:")
            st.title("Sistem Deteksi Huruf Alfabet Bahasa Isyarat Indonesia")
        with right_column:
            st_lottie(hello, height=300)
    if 'about' not in st.session_state:
        st.session_state['about'] = False
    if st.button('Lihat Selengkapnya'):
        st.session_state['about'] = not st.session_state['about']
    if st.session_state['about']:
        # ---- WHAT I DO ----
        with st.container():
            st.write("---")
            left_column, right_column = st.columns(2)
            with left_column:
                st_lottie(lottie_coding, height=300)
            with right_column:
                st.header("Tentang Aplikasi")
                st.write("##")
                st.write(
                    """
                    Sistem ini dikembangkan dengan menggunakan Machine Learning dengan metode random forest:
                    - Data gambar yang digunakan berjumlah 5200 yang berisi huruf dari A-Z.
                    - Sistem ini memiliki akurasi 100% untuk 1 tangan dan 99,84% untuk 2 tangan.
                    - Sistem ini dapat mendeteksi dan menerjemahkan huruf alfabet bahasa isyarat indonesia ke dalam teks dan suara.
                    """
                )

app()

