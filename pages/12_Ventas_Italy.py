# import streamlit as st
# import pandas as pd
# import geopandas as gpd
# import matplotlib.pyplot as plt
# import contextily as ctx

# # Sample sales data for locations in Spain
# data = {
#     'Province': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Zaragoza', 'Málaga', 'Murcia'],
#     'Sales': [200000, 180000, 150000, 170000, 130000, 140000, 120000]
# }

# # Create a DataFrame
# df = pd.DataFrame(data)

# # Load Spanish provinces shapefile
# # Make sure to update the path to where you have saved the shapefile or GeoJSON
# shapefile_path = 'gadm41_ESP_shp/gadm41_ESP_2.shp'  # Replace with the correct path
# gdf_provinces = gpd.read_file(shapefile_path)

# # Merge sales data with provinces GeoDataFrame
# gdf_provinces = gdf_provinces.merge(df, left_on='NAME_2', right_on='Province', how='left')

# # Streamlit app
# st.title('Sales Geomap for Spain by Province')

# st.markdown("""
# This app visualizes sales data for various provinces in Spain. The color intensity of each province corresponds to the sales volume at that location.
# """)

# # Plotting the map
# fig, ax = plt.subplots(1, 1, figsize=(10, 15))
# gdf_provinces.plot(column='Sales', ax=ax, legend=True, cmap='OrRd', edgecolor='black', missing_kwds={"color": "lightgrey", "label": "No data"}, legend_kwds={'shrink': 0.42}, linewidth=.1)

# # Add basemap
# ctx.add_basemap(ax, crs=gdf_provinces.crs.to_string(), source=ctx.providers.CartoDB.Positron)


# plt.title('Sales Data Geomap for Spain by Province')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')

# Show the map in Streamlit
# st.pyplot(fig)

import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import requests
import numpy as np

# Sample sales data for different regions in Italy
data = {
    'Region': ['Lombardia', 'Lazio', 'Campania', 'Sicilia', 'Veneto'],
    'Sales': [30000, 22000, 18000, 16000, 14000]
}

df = pd.DataFrame(data)

# URL to the GeoJSON file for Italy regions
geojson_url = 'https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson'

# Download the GeoJSON file
response = requests.get(geojson_url)
geojson_data = response.json()

# Load the GeoJSON data into a GeoDataFrame
geo_data = gpd.GeoDataFrame.from_features(geojson_data['features'])

# Merge sales data with GeoDataFrame
geo_data = geo_data.rename(columns={"reg_name": "Region"})
geo_data['Region'] = geo_data['Region'].str.title()
geo_data = geo_data.merge(df, on="Region", how="left")

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
        title="Sales by Region in Italy",
        
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
st.title("Sales Geomap for Italy")
st.write("Interactive geomap displaying sales data for different regions in Italy. Regions with no sales data are shown in grey.")

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
