from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent / 'util'))

from load_data import load_data
import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import requests
import numpy as np
from util.expander import set_expander_region, set_expander_client, set_expander_category, set_expander_brand, set_expander_product, set_expander_salesperon, set_date, adjust_for_february
from util.filter_data import filter_data
from util.build_tablet import build_tablet
from util.plot_lineChart import plot_lineChart
from util.plot_barChart import plot_barChart
import re

load_data()
zip_code_to_province_spain_df = pd.read_csv("data/zip_code_to_province_spain.csv", index_col=0)
zip_code_to_province_spain_dict = zip_code_to_province_spain_df.set_index('ZIP Code Range').squeeze().to_dict()
st.session_state['region_ls'] = list(zip_code_to_province_spain_dict.values())


col1, col2, col3, col4 = st.columns(4)
col5, col6, col7, col8 = st.columns(4)

with col1:
    st.image('ZhonghuiTitle.png', width=320)

with col2:
    st.session_state['region_filter'] = set_expander_region()

with col3:
    st.session_state['customer_type_filter'] = set_expander_client()
        
with col4:
    st.session_state['category_filter'] = set_expander_category()
        
with col5:
    st.markdown('<h3 class="custom-header", style="text-align: center;">Análisis Venta Global</h3>', unsafe_allow_html=True)

with col6:
    st.session_state['brand_filter'] = set_expander_brand()
        
with col7:
    st.session_state['product_filter'] = set_expander_product()

with col8:
    st.session_state['seller_filter'] = set_expander_salesperon()

start_date = '2023-01-01'
end_date = '2023-12-31'

st.session_state['start_date'], st.session_state['end_date'] = set_date(start_date, end_date)

st.session_state['start_date_past'] = adjust_for_february(st.session_state['start_date'])
st.session_state['end_date_past'] = adjust_for_february(st.session_state['end_date'])

selected_df, selected_past_df = filter_data(["ES"], st.session_state['product_filter'], st.session_state['brand_filter'], st.session_state['customer_type_filter'], st.session_state['seller_filter'], st.session_state['category_filter'], st.session_state['start_date_past'], st.session_state['start_date'], st.session_state['end_date'], st.session_state['end_date_past'])


def zip_code_to_province_spain(zip_code, zip_code_to_province_spain_dict):
    import re

    try:
        return zip_code_to_province_spain_dict[re.sub(r"(^[0-9]{2})([0-9]{3})", r'\1xxx', str(zip_code))]
    except:
        return "unknown"
    
selected_df['Region'] = selected_df["Sell-to Post Code"].apply(lambda x: zip_code_to_province_spain(x, zip_code_to_province_spain_dict))



    # st.experimental_rerun()

selected_df = selected_df[selected_df['Region'].isin(st.session_state['region_filter'])]


selected_customer_df = selected_df[['Customer Name', 'Amount']].groupby(['Customer Name']).sum()
selected_customer_past_df = selected_past_df[['Customer Name', 'Amount']].groupby(['Customer Name']).sum()
selected_customer_all_df =  selected_customer_df.merge(selected_customer_past_df, how="outer", on="Customer Name", suffixes=["_now", "_past"]).reset_index().rename({"Amount_now": "Ventas", "Amount_past":"Ventas Año Ant."}, axis=1)

build_tablet(selected_df, selected_past_df)

plot_lineChart(selected_df, selected_past_df)

plot_barChart(selected_customer_all_df)


# st.write(selected_df.head())
# st.write(selected_df['Province'].unique())

# Sample sales data for different regions in Spain
# data = {
#     'Region': ['Madrid', 'Barcelona', 'Sevilla', 'Valencia', 'A Coruña'],
#     'Sales': [25000, 20000, 15000, 12000, 8000]
# }

# df = pd.DataFrame(data)

selected_df = selected_df[selected_df['Region']!=-1]
# URL to the GeoJSON file for Spain regions
geojson_url = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/spain-provinces.geojson'

# Download the GeoJSON file
response = requests.get(geojson_url)
geojson_data = response.json()

# Load the GeoJSON data into a GeoDataFrame
geo_data = gpd.GeoDataFrame.from_features(geojson_data['features'])

# Merge sales data with GeoDataFrame
geo_data = geo_data.rename(columns={"name": "Region"})

geo_data['Region'] = geo_data['Region'].str.title()
geo_data = geo_data.merge(selected_df.groupby("Region")['Amount'].sum().reset_index().rename({"Amount": "Sales"}, axis=1), on="Region", how="left")

# Set NaN sales to a special value to distinguish them
geo_data['Sales'] = geo_data['Sales'].fillna(0)

# Function to create the Plotly figure
def create_geomap(geo_data):
    fig = px.choropleth(
        geo_data, 
        geojson=geo_data.geometry, 
        locations=geo_data.index, 
        color="Sales",
        hover_name="Region",
        projection="mercator",
        title="Sales by Region in Spain",
        
        color_continuous_scale=[
            (0.0, "lightgrey"),    # No sales data
            (1E-5, "#FFFFFF"), (1, "#FF0000")
        ],
        range_color=(0, geo_data['Sales'].max()),
    )
    

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),
                  width=1500, 
                  height=800)
    return fig

# Streamlit app
st.title("Sales Geomap for Spain")
st.write("Interactive geomap displaying sales data for different regions in Spain. Regions with no sales data are shown in grey.")

fig = create_geomap(geo_data)
st.plotly_chart(fig)


# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import geopandas as gpd
# import requests
# import numpy as np

# # Sample sales data for different regions in Spain
# data = {
#     'Region': ['Madrid', 'Barcelona', 'Sevilla', 'Valencia', 'A Coruña'],
#     'Sales': [25000, 20000, 15000, 12000, 80000]
# }

# df = pd.DataFrame(data)

# # URL to the GeoJSON file for Spain regions
# geojson_url = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/spain-provinces.geojson'

# # Download the GeoJSON file
# response = requests.get(geojson_url)
# geojson_data = response.json()

# # Load the GeoJSON data into a GeoDataFrame
# geo_data = gpd.GeoDataFrame.from_features(geojson_data['features'])

# # Merge sales data with GeoDataFrame
# geo_data = geo_data.rename(columns={"name": "Region"})
# geo_data['Region'] = geo_data['Region'].str.title()
# geo_data = geo_data.merge(df, on="Region", how="left")

# # Set NaN sales to a special value to distinguish them
# geo_data['Sales'] = geo_data['Sales'].fillna(-1)

# # Function to create the Plotly figure
# def create_geomap(geo_data):
#     # Transform sales data to log scale, handling -1 as a special case for NaNs
#     geo_data['Log_Sales'] = geo_data['Sales'].apply(lambda x: np.log10(x) if x > 0 else 0)
    
#     fig = px.choropleth(
#         geo_data, 
#         geojson=geo_data.geometry, 
#         locations=geo_data.index, 
#         color="Log_Sales",
#         hover_name="Region",
#         hover_data={"Sales": True, "Region": True},
#         projection="mercator",
#         title="Sales by Region in Spain (Log Scale)",
#         color_continuous_scale=[
#             (0.0, "lightgrey"),    # No sales data
#             (0.00001, "white"), # Start of sales data
#             (1.0, "darkblue")
#         ],
#         labels={'Log_Sales': 'Log(Sales)'}
#     )

#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     fig.update_coloraxes(colorbar_title="Log(Sales)")
#     return fig

# # Streamlit app
# st.title("Sales Geomap for Spain")
# st.write("Interactive geomap displaying sales data for different regions in Spain. Regions with no sales data are shown in grey.")

# fig = create_geomap(geo_data)
# st.plotly_chart(fig)
