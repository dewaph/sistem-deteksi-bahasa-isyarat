import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import home
import belajar
import terjemahan
import praktek
import subprocess
import os

# # custom tampilan aplikasi
# icon = Image.open('logo/bisindo.png')
# st.set_page_config(page_title='Sistem Deteksi BISINDO', page_icon=icon, layout='wide',initial_sidebar_state='collapsed')

with open( "style\style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
# hilangkan 3 garis dan tulisan streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# sidebar menu
st.sidebar.image('logo/bisindo.png', width=100)
st.sidebar.markdown("<div><h1 style='display:inline-block'>Sistem Deteksi Bahasa Isyarat Indonesia</h1></div>", unsafe_allow_html=True)
with st.sidebar:
    page = option_menu(
        menu_title="Menu Utama",  # required
        options=["Beranda", "Kamus", "Praktek", "Terjemahan", "Logout"],  # required
        icons=["house", "book", "hand-index-thumb", "translate", "bi-box-arrow-right"],  # optional
        menu_icon="app-indicator",  # optional
        default_index=0,  # optional
        styles={
            "container": {"padding": "5!important"},
            "icon": {"color": "yellow", "font-size": "16px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#292922"},
            "nav-link-selected": {"background-color": "#018735"}}
    )
# Fungsi untuk mengubah halaman berdasarkan tautan yang dipilih
def change_page(page):
    if page == "Beranda":
        home.app()
    elif page == "Kamus":
        belajar.app()
    elif page == "Praktek":
        praktek.app()
    elif page == "Terjemahan":
        terjemahan.app()
    elif page == "Logout":
        subprocess.Popen(["streamlit", "run", "index.py"])
        os._exit(0)  # Menutup index.py

# Tampilkan halaman yang dipilih
change_page(page)


