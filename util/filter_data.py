import streamlit as st
import pandas as pd

@st.cache_data
def filter_data(country_filter, product_filter, brand_filter, customer_type_filter, seller_filter, category_filter, start_date_past, start_date, end_date, end_date_past):
    salesHeader_selected_df = st.session_state.salesHeader_df[(st.session_state.salesHeader_df['Posting Date'] >= pd.to_datetime(start_date)) & (st.session_state.salesHeader_df['Posting Date'] <= pd.to_datetime(end_date)) & 
                                            (st.session_state.salesHeader_df['Sell-to Country_Region Code'].isin(country_filter)) ] 
    salesLine_selected_df = st.session_state.salesLine_df[(st.session_state.salesLine_df['Product No_'].isin(product_filter)) & st.session_state.salesLine_df['Brand Code'].isin(brand_filter)]
    dimension_selected_df = st.session_state.dimension_df[st.session_state.dimension_df['Dimension Name'].isin(customer_type_filter)]
    salesPerson_selected_df = st.session_state.salesPerson_df[st.session_state.salesPerson_df['Salesperson Name'].isin(seller_filter)]
    itemCategory_selected_df = st.session_state.itemCategory_df[st.session_state.itemCategory_df['Item Category Description'].isin(category_filter)]

    salesHeader_selected_past_df = st.session_state.salesHeader_df[(st.session_state.salesHeader_df['Posting Date'] >= pd.to_datetime(start_date_past)) & (st.session_state.salesHeader_df['Posting Date'] <= pd.to_datetime(end_date_past)) & 
                                            (st.session_state.salesHeader_df['Sell-to Country_Region Code'].isin(country_filter)) ] 


    selected_df = dimension_selected_df.merge(st.session_state.customer_df, how='inner', left_on='Dimension Code', right_on='Global Dimension 1 Code')\
    .merge(salesHeader_selected_df, how='inner', left_on='Customer No_', right_on="Sell-to Customer No_")\
    .merge(salesPerson_selected_df, how='inner', left_on='Salesperson Code', right_on='Salesperson Code')\
    .merge(salesLine_selected_df, how='inner', left_on='Document No_', right_on='Document No_')\
    .merge(itemCategory_selected_df , how='inner', left_on='Item Category Code', right_on='Item Category Code').dropna()

    selected_past_df = dimension_selected_df.merge(st.session_state.customer_df, how='inner', left_on='Dimension Code', right_on='Global Dimension 1 Code')\
    .merge(salesHeader_selected_past_df, how='inner', left_on='Customer No_', right_on="Sell-to Customer No_")\
    .merge(salesPerson_selected_df, how='inner', left_on='Salesperson Code', right_on='Salesperson Code')\
    .merge(salesLine_selected_df, how='inner', left_on='Document No_', right_on='Document No_')\
    .merge(itemCategory_selected_df , how='inner', left_on='Item Category Code', right_on='Item Category Code').dropna()

    return selected_df, selected_past_df