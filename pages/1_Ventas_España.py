import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Sample sales data for locations in Spain
data = {
    'Province': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Zaragoza', 'Málaga', 'Murcia'],
    'Sales': [200000, 180000, 150000, 170000, 130000, 140000, 120000]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Load Spanish provinces shapefile
# Make sure to update the path to where you have saved the shapefile or GeoJSON
shapefile_path = 'gadm41_ESP_shp/gadm41_ESP_2.shp'  # Replace with the correct path
gdf_provinces = gpd.read_file(shapefile_path)

# Merge sales data with provinces GeoDataFrame
gdf_provinces = gdf_provinces.merge(df, left_on='NAME_2', right_on='Province', how='left')

# Streamlit app
st.title('Sales Geomap for Spain by Province')

st.markdown("""
This app visualizes sales data for various provinces in Spain. The color intensity of each province corresponds to the sales volume at that location.
""")

# Plotting the map
fig, ax = plt.subplots(1, 1, figsize=(10, 15))
gdf_provinces.plot(column='Sales', ax=ax, legend=True, cmap='OrRd', edgecolor='black', missing_kwds={"color": "lightgrey", "label": "No data"}, legend_kwds={'shrink': 0.42}, linewidth=.1)

# Add basemap
ctx.add_basemap(ax, crs=gdf_provinces.crs.to_string(), source=ctx.providers.CartoDB.Positron)


plt.title('Sales Data Geomap for Spain by Province')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Show the map in Streamlit
st.pyplot(fig)
