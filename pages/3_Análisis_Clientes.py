# from pathlib import Path
# import sys

# sys.path.append(str(Path(__file__).resolve().parent.parent / 'util'))

# from load_data import load_data
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import geopandas as gpd
# import requests
# import numpy as np
# from util.expander import set_expander_country, set_expander_client, set_expander_category, set_expander_brand, set_expander_product, set_expander_salesperon, set_date, adjust_for_february
# from util.filter_data import filter_data
# from util.build_tablet import build_tablet
# from util.plot_lineChart import plot_lineChart
# from util.plot_barChart import plot_barChart
# import re

# load_data()

# col1, col2, col3, col4 = st.columns(4)
# col5, col6, col7, col8 = st.columns(4)

# with col1:
#     st.image('ZhonghuiTitle.png', width=320)

# with col2:
#     st.session_state['country_filter'] = set_expander_country(default=['ES'], options=['ES'])

# with col3:
#     st.session_state['customer_type_filter'] = set_expander_client()
        
# with col4:
#     st.session_state['category_filter'] = set_expander_category()
        
# with col5:
#     st.markdown('<h3 class="custom-header", style="text-align: center;">Análisis Venta Global</h3>', unsafe_allow_html=True)

# with col6:
#     st.session_state['brand_filter'] = set_expander_brand()
        
# with col7:
#     st.session_state['product_filter'] = set_expander_product()

# with col8:
#     st.session_state['seller_filter'] = set_expander_salesperon()

# start_date = '2023-01-01'
# end_date = '2023-12-31'

# st.session_state['start_date'], st.session_state['end_date'] = set_date(start_date, end_date)

# st.session_state['start_date_past'] = adjust_for_february(st.session_state['start_date'])
# st.session_state['end_date_past'] = adjust_for_february(st.session_state['end_date'])

# selected_df, selected_past_df = filter_data(st.session_state['country_filter'], st.session_state['product_filter'], st.session_state['brand_filter'], st.session_state['customer_type_filter'], st.session_state['seller_filter'], st.session_state['category_filter'], st.session_state['start_date_past'], st.session_state['start_date'], st.session_state['end_date'], st.session_state['end_date_past'])

# st.write(selected_df.head())

import pandas as pd
import geopandas as gpd
import folium
import streamlit as st
from folium.features import GeoJsonTooltip
from streamlit.components.v1 import html

# Sample sales data for various locations (Replace with your actual data)
data = {
    'Sell-to Country_Region Code': ['US', 'CA', 'BR', 'IN', 'CN', 'AU', 'RU'],
    'Amount': [200000, 180000, 150000, 170000, 130000, 140000, 120000]
}
selected_df = pd.DataFrame(data)

# Load country map and sales data
country_map_df = pd.read_csv("data/country_map.csv", index_col=0)
country_map = country_map_df.drop(["3-Digit Code"], axis=1).set_index("2-Digit Code").squeeze().to_dict()
map_df = selected_df.groupby(['Sell-to Country_Region Code'])['Amount'].sum().reset_index()
map_df['Country'] = map_df['Sell-to Country_Region Code'].map(country_map)
map_df = map_df.drop(['Sell-to Country_Region Code'], axis=1).rename({"Amount": "Sales"}, axis=1)

# Load world countries shapefile
shapefile_path = gpd.datasets.get_path('naturalearth_lowres')
gdf_countries = gpd.read_file(shapefile_path)

# Merge sales data with countries GeoDataFrame
gdf_countries = gdf_countries.merge(map_df, left_on='name', right_on='Country', how='left')

# Streamlit app
st.title('Global Sales Geomap')

st.markdown("""
This app visualizes sales data for various countries. The color intensity of each country corresponds to the sales volume at that location.
""")

sales_max = map_df['Sales'].max()

# Create a folium map
m = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodb positron')

# Define a function to style the GeoJson based on sales
def style_function(feature):
    sales = feature['properties']['Sales']
    return {
        'fillOpacity': 0.7,
        'weight': 0.5,
        'fillColor': '#808080' if sales is None else '#%02x%02x%02x' % (int((sales / sales_max) * 255), 0, 255 - int((sales / sales_max) * 255))
    }

# Add the GeoJson layer to the map
geojson = folium.GeoJson(
    gdf_countries,
    style_function=style_function,
    tooltip=GeoJsonTooltip(fields=['name', 'Sales'], aliases=['Country', 'Sales'], localize=True)
).add_to(m)

# JavaScript to handle the click event and update the hidden input field
click_js = """
<script>
    function onMapClick(e) {
        var layer = e.layer;
        if (layer.feature) {
            var country = layer.feature.properties.name;
            var input = parent.document.getElementById('country-input');
            input.value = country;
            input.dispatchEvent(new Event('input'));
        }
    }
    var map = document.querySelector('.folium-map').__folium;
    map.on('click', onMapClick);
</script>
"""

# Save the map to an HTML file and display in Streamlit
m.save('map.html')
st.components.v1.html(m._repr_html_() + click_js, width=1400, height=800)

# JavaScript to handle the input event and update the session state
input_js = """
<script>
    document.getElementById('country-input').addEventListener('input', function() {
        const country = this.value;
        const message = {type: 'country', country: country};
        window.parent.postMessage(message, '*');
    });
</script>
<input type="hidden" id="country-input" />
"""

# Display the hidden input and JavaScript
html(input_js, height=0, width=0)

# Initialize session state
if 'country' not in st.session_state:
    st.session_state['country'] = ''

# Function to update session state
def update_country():
    js_code = """
    <script>
        window.addEventListener("message", (event) => {
            if (event.data.type && event.data.type === 'country') {
                const country = event.data.country;
                const input = window.parent.document.getElementById('country-input');
                input.value = country;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                window.parent.document.dispatchEvent(new Event('update-country'));
            }
        });
    </script>
    """
    html(js_code, height=0, width=0)

# Call function to ensure session state updates
update_country()

# Function to capture the updated country value
def get_country():
    country = st.text_input("Country", key="country-input")
    if country:
        st.session_state['country'] = country
    return country

country = get_country()

# Display the clicked country in Streamlit
if st.session_state['country']:
    st.write(f"You clicked on: {st.session_state['country']}")
