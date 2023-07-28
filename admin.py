import streamlit as st
from streamlit_option_menu import option_menu
import dashboard
import testing
import training
import data
import kamus
import os
import subprocess
import landmark


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
st.sidebar.markdown("<div><h1 style='display:inline-block'>Halaman Admin</h1></div>", unsafe_allow_html=True)
with st.sidebar:
    page = option_menu(
        menu_title="Menu Admin",  # required
        options=["Dashboard", "Edit Kamus", "Tambah Data", "Preprocessing data", "Training", "Testing", "Logout"],  # required
        icons=["bi-speedometer", "bi-pencil-square", "bi-database-add", "bi-activity", "bi-bar-chart-fill", "bi-webcam", "bi-box-arrow-right"],  # optional
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
    if page == "Dashboard":
        dashboard.app()
    elif page == "Tambah Data":
        data.app()
    elif page == "Edit Kamus":
        kamus.app()
    elif page == "Preprocessing data":
        landmark.app()
    elif page == "Training":
        training.app()
    elif page == "Testing":
        testing.app()
    elif page == "Logout":
        subprocess.Popen(["streamlit", "run", "index.py"])
        os._exit(0)  # Menutup index.py



# Tampilkan halaman yang dipilih
change_page(page)


