import streamlit as st
import hydralit_components as hc
import isyarat
import suara

def app():
    over_theme = {'txc_inactive': '#FFFF01', 'menu_background': '#018735', 'txc_active': 'white'}

    menu_data = [
        {'icon': "bi bi-ear-fill", 'label': "Isyarat Tangan"},
        {'icon': "bi bi-soundwave", 'label': "Suara"},
    ]

    menu_id = hc.nav_bar(menu_definition=menu_data,
                         override_theme=over_theme,
                         sticky_nav=True,  # at the top or not
                         sticky_mode='pinned',  # jumpy or not-jumpy, but sticky or pinned
                         )

    st.title("Terjemahan")

    def change_menu(menu_id):
        if menu_id == "Isyarat Tangan":
            isyarat.app()
        elif menu_id == "Suara":
            suara.app()

    # Tampilkan halaman yang dipilih
    change_menu(menu_id)