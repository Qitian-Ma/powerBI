
    
def load_data():
    import streamlit as st
    import pandas as pd
    import functools

    file_ls = ['salesHeader_df', 'salesLine_df', 'brandCode_ls', 'productNo_ls', 'country_ls', 'customer_df', 'dimension_df', 'dimension_ls', 'productGroup_df', 'itemCategory_df', 'itemCategory_ls', 'salesPerson_df', 'salesPerson_ls'] 
    
    
    if functools.reduce(lambda a, b: a and b, file_ls) == True:
        return

    @st.cache_data
    def load_sales_data():
        
        salesLine_df = pd.read_csv(r"data\salesLine_2324.csv", index_col=0)
        salesHeader_df = pd.read_csv(r"data\salesHeader_2324.csv", index_col=0)
        salesHeader_df['Posting Date'] = salesHeader_df['Posting Date'].apply(lambda time: pd.to_datetime(time, format='%Y-%m-%d'))

        salesHeader_df['Sell-to Country_Region Code'] = salesHeader_df['Sell-to Country_Region Code'].fillna(salesHeader_df['Bill-to Country_Region Code']).fillna(salesHeader_df['VAT Country_Region Code']).fillna(salesHeader_df["Ship-to Country_Region Code"])
        salesHeader_df['Sell-to County'] = salesHeader_df['Sell-to County'].fillna(salesHeader_df['Bill-to County']).fillna(salesHeader_df['Ship-to County'])
        salesHeader_df['Sell-to Post Code'] = salesHeader_df['Sell-to Post Code'].fillna(salesHeader_df['Bill-to Post Code']).fillna(salesHeader_df['Ship-to Post Code'])

        salesHeader_df.drop(['Bill-to Country_Region Code', 'VAT Country_Region Code', 'Bill-to County', 'Bill-to Post Code', "Ship-to Country_Region Code", 'Ship-to County', 'Ship-to Post Code'], axis=1, inplace=True)


        return salesHeader_df, salesLine_df, salesLine_df['Brand Code'].dropna().unique().tolist(), salesLine_df['Product No_'].unique().tolist(), salesHeader_df['Sell-to Country_Region Code'].unique().tolist()

    @st.cache_data
    def load_customer_data():
        customer_df = pd.read_csv(r"data\customer.csv", index_col=0)
        return customer_df

    @st.cache_data
    def load_dimension_data():
        dimension_df = pd.read_csv(r"data\dimension.csv", index_col=0)
        return dimension_df, dimension_df['Dimension Name'].unique().tolist()

    @st.cache_data
    def load_classification_data():
        productGroup_df = pd.read_csv(r"data\productGroup.csv", index_col=0)
        itemCategory_df = pd.read_csv(r"data\itemCategory.csv", index_col=0)
        return productGroup_df, itemCategory_df, itemCategory_df['Item Category Description'].unique().tolist()

    @st.cache_data
    def load_salesPerson_data():
        salesPerson_df = pd.read_csv(r"data\salesPerson.csv", index_col=0)
        return salesPerson_df, salesPerson_df['Salesperson Name'].unique().tolist()

    salesHeader_df, salesLine_df, brandCode_ls, productNo_ls, country_ls = load_sales_data()
    customer_df = load_customer_data()
    dimension_df, dimension_ls = load_dimension_data()
    productGroup_df, itemCategory_df, itemCategory_ls = load_classification_data()
    salesPerson_df, salesPerson_ls = load_salesPerson_data()

    st.session_state['salesHeader_df'] = salesHeader_df
    st.session_state['salesLine_df'] = salesLine_df
    st.session_state['brandCode_ls'] = brandCode_ls
    st.session_state['productNo_ls'] = productNo_ls
    st.session_state['country_ls'] = country_ls
    st.session_state['customer_df'] = customer_df
    st.session_state['dimension_df'] = dimension_df
    st.session_state['dimension_ls'] = dimension_ls
    st.session_state['productGroup_df'] = productGroup_df
    st.session_state['itemCategory_df'] = itemCategory_df
    st.session_state['itemCategory_ls'] = itemCategory_ls
    st.session_state['salesPerson_df'] = salesPerson_df
    st.session_state['salesPerson_ls'] = salesPerson_ls
