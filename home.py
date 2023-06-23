import streamlit as st
import requests
from streamlit_lottie import st_lottie


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_kUtZCR7Zyk.json")
hello = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_3vbOcw.json")

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
            st_lottie(hello, height=300, key="robot")
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
                st_lottie(lottie_coding, height=300, key="coding")
            with right_column:
                st.header("Tentang Aplikasi")
                st.write("##")
                st.write(
                    """
                    On my YouTube channel I am creating tutorials for people who:
                    - are looking for a way to leverage the power of Python in their day-to-day work.
                    - are struggling with repetitive tasks in Excel and are looking for a way to use Python and VBA.
                    - want to learn Data Analysis & Data Science to perform meaningful and impactful analyses.
                    - are working with Excel and found themselves thinking - "there has to be a better way."

                    If this sounds interesting to you, consider subscribing and turning on the notifications, so you don’t miss any content.
                    """
                )
                st.write("[YouTube Channel >](https://youtube.com/c/CodingIsFun)")


app()
