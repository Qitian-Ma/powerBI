import streamlit as st
from util.button_action import clear_settings_country, clear_settings_client, clear_settings_category, \
                               clear_settings_brand, clear_settings_product, clear_settings_seller, \
                               select_all_country, select_all_client, select_all_category, \
                               select_all_brand, select_all_product, select_all_seller

def set_expander_country(default=None, options=None):
    with st.expander("País"):
        col21, col22 = st.columns(2)
        with col21:
            st.button('Clear Selections', on_click=clear_settings_country, key='21')
        with col22:
            st.button('Select All', on_click=select_all_country, key='22', type="primary", use_container_width=True)

        if default is None or options is None:
            country_filter = st.multiselect('País', default=st.session_state.country_ls, options=st.session_state.country_ls, label_visibility ="collapsed", key='selected_options_country')

    return country_filter

def set_expander_client():
    with st.expander("Tipo Cliente"):
        col31, col32 = st.columns(2)
        with col31:
            st.button('Clear Selections', on_click=clear_settings_client, key='31')
        with col32:
            st.button('Select All', on_click=select_all_client, key='32', type="primary", use_container_width=True)
        customer_type_filter = st.multiselect('Tipo Cliente', default=st.session_state.dimension_ls, options=st.session_state.dimension_ls, label_visibility ="collapsed", key='selected_options_client')

    return customer_type_filter

def set_expander_category():
    with st.expander("Categoría, Subcategoría"):
        col41, col42 = st.columns(2)
        with col41:
            st.button('Clear Selections', on_click=clear_settings_category, key='41')
        with col42:
            st.button('Select All', on_click=select_all_category, key='42', type="primary", use_container_width=True)
        category_filter = st.multiselect('Categoría, Subcategoría', default=st.session_state.itemCategory_ls, options=st.session_state.itemCategory_ls, label_visibility ="collapsed", key='selected_options_category')

    return category_filter    
        
def set_expander_brand():
    with st.expander("Marca"):
        col61, col62 = st.columns(2)
        with col61:
            st.button('Clear Selections', on_click=clear_settings_brand, key='61')
        with col62:
            st.button('Select All', on_click=select_all_brand, key='62', type="primary", use_container_width=True)
        brand_filter = st.multiselect('Marca', default=st.session_state.brandCode_ls, options=st.session_state.brandCode_ls, label_visibility ="collapsed", key='selected_options_brand')
    return brand_filter

def set_expander_product():
    with st.expander("Producto"):
        col71, col72 = st.columns(2)
        with col71:
            st.button('Clear Selections', on_click=clear_settings_product, key='71')
        with col72:
            st.button('Select All', on_click=select_all_product, key='72', type="primary", use_container_width=True)
        product_filter = st.multiselect('Producto', default=st.session_state.productNo_ls, options=st.session_state.productNo_ls, label_visibility ="collapsed", key='selected_options_product')
    return product_filter

def set_expander_salesperon():
    with st.expander("Vendedor"):
        col81, col82 = st.columns(2)
        with col81:
            st.button('Clear Selections', on_click=clear_settings_seller, key='81')
        with col82:
            st.button('Select All', on_click=select_all_seller, key='82', type="primary", use_container_width=True)
        seller_filter = st.multiselect('Vendedor', default=st.session_state.salesPerson_ls, options=st.session_state.salesPerson_ls, label_visibility ="collapsed", key='selected_options_seller')

    return seller_filter

def set_date(start_date, end_date):
    import pandas as pd

    col14, col15, col16 = st.columns([1, 1, 6])

    with col14:
        if 'start_date' not in st.session_state:
            start_date = st.date_input('Start date', pd.to_datetime(start_date))
            st.session_state['start_date'] = start_date
        else:
            start_date = st.date_input('Start date', st.session_state['start_date'])


    with col15:
        if 'end_date' not in st.session_state:
            end_date = st.date_input('End date', pd.to_datetime(end_date))
            st.session_state['end_date'] = end_date
        else:
            end_date = st.date_input('End date', st.session_state['end_date'])

    # start_date = datetime.date(2022, 4, 30)
    # end_date = datetime.date(2024, 6, 6)

    with col16:
        date_range = st.slider('Fecha', min_value=pd.to_datetime(start_date), max_value=pd.to_datetime(end_date), value=(pd.Timestamp(start_date).to_pydatetime(), pd.Timestamp(end_date).to_pydatetime()), format="YYYY-MM-DD")
        start_date = date_range[0]
        end_date = date_range[1]
        if start_date != st.session_state.start_date or end_date != st.session_state.end_date:
            st.session_state.start_date = start_date
            st.session_state.end_date = end_date
            st.rerun()

    return start_date, end_date

def adjust_for_february(date, mov=1):
    from datetime import datetime
    # Get the previous year
    previous_year = date.year - mov
    
    # Check if the current date is in February
    if date.month == 2:
        # Check if the day is 28 or more
        if date.day > 28:
            # Adjust to the 27th of February of the previous year if the date is 28 or more
            adjusted_date = datetime(previous_year, 2, 27)
        else:
            # Otherwise, adjust to the same day in February of the previous year
            adjusted_date = datetime(previous_year, 2, date.day)
    else:
        # If the month is not February, simply adjust the year
        adjusted_date = date.replace(year=previous_year)
    
    return adjusted_date