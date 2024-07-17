import streamlit as st

@st.cache_data
def build_tablet(selected_df, selected_past_df):
    from .tablet import get_html, custom_css
    import streamlit as st
    import pandas as pd
    import numpy as np

    col9, col10, col11, col12, col13 = st.columns(5, gap='large')

    with col9:
        current_sales = selected_df['Amount'].sum()
        previous_sales = selected_past_df['Amount'].sum()

        try:
            diff_percentage = ((current_sales - previous_sales) / previous_sales) * 100
        except:
            diff_percentage = np.NaN

        st.markdown(custom_css, unsafe_allow_html=True)

        sales_widget_html = get_html("Ventas", current_sales, previous_sales, diff_percentage, euro=True)

        st.markdown(sales_widget_html, unsafe_allow_html=True)

    with col10:
        current_sales = selected_df['Document No_'].nunique()
        previous_sales = selected_past_df['Document No_'].nunique()

        try:
            diff_percentage = ((current_sales - previous_sales) / previous_sales) * 100
        except:
            diff_percentage = np.NaN

        st.markdown(custom_css, unsafe_allow_html=True)

        sales_widget_html = get_html("No. Facturas", current_sales, previous_sales, diff_percentage)

        st.markdown(sales_widget_html, unsafe_allow_html=True)


    with col11:
        try:
            current_sales = int(selected_df['Amount'].sum() / selected_df['Document No_'].nunique())
            previous_sales = int(selected_past_df['Amount'].sum() / selected_past_df['Document No_'].nunique())
        except:
            current_sales = np.NaN
            previous_sales = np.NaN

        try:
            diff_percentage = ((current_sales - previous_sales) / previous_sales) * 100
        except:
            diff_percentage = np.NaN

        st.markdown(custom_css, unsafe_allow_html=True)

        sales_widget_html = get_html("Ticket Medio", current_sales, previous_sales, diff_percentage)

        st.markdown(sales_widget_html, unsafe_allow_html=True)


    with col12:
        current_sales = selected_df['Quantity'].sum()
        previous_sales = selected_past_df['Quantity'].sum()

        try:
            diff_percentage = ((current_sales - previous_sales) / previous_sales) * 100
        except:
            diff_percentage = np.NaN

        st.markdown(custom_css, unsafe_allow_html=True)

        sales_widget_html = get_html("No. Unidades", current_sales, previous_sales, diff_percentage)

        st.markdown(sales_widget_html, unsafe_allow_html=True)

    with col13:
        current_sales = selected_df['Product No_'].nunique()
        previous_sales = selected_past_df['Product No_'].nunique()
        
        try:
            diff_percentage = ((current_sales - previous_sales) / previous_sales) * 100
        except:
            diff_percentage = np.NaN

        st.markdown(custom_css, unsafe_allow_html=True)

        sales_widget_html = get_html("No. Artículos Distintos", current_sales, previous_sales, diff_percentage)

        st.markdown(sales_widget_html, unsafe_allow_html=True)
