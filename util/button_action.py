import streamlit as st

def clear_settings_country():
    st.session_state.selected_options_country = []

def clear_settings_client():
    st.session_state.selected_options_client = []

def clear_settings_category():
    st.session_state.selected_options_category = []

def clear_settings_brand():
    st.session_state.selected_options_brand = []

def clear_settings_product():
    st.session_state.selected_options_product = []

def clear_settings_seller():
    st.session_state.selected_options_seller = []

def select_all_country():
    st.session_state.selected_options_country = ['ES', 'IT']

def select_all_client():
    st.session_state.selected_options_client = st.session_state.dimension_ls

def select_all_category():
    st.session_state.selected_options_category = st.session_state.itemCategory_ls

def select_all_brand():
    st.session_state.selected_options_brand = st.session_state.brandCode_ls

def select_all_product():
    st.session_state.selected_options_product = st.session_state.productNo_ls

def select_all_seller():   
    st.session_state.selected_options_seller = st.session_state.salesPerson_ls
