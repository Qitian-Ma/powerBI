import streamlit as st
import pandas as pd
import numpy as np

from util.load_data import load_data
from util.expander import set_expander_country, set_expander_client, set_expander_category, set_expander_brand, set_expander_product, set_expander_salesperon, set_date, adjust_for_february
from util.build_tablet import build_tablet
from util.filter_data import filter_data
from util.plot_lineChart import plot_lineChart
from util.plot_barChart import plot_barChart
import geopandas as gpd
import folium
from folium.features import GeoJson, GeoJsonTooltip
from datetime import datetime, timedelta
import warnings
from streamlit_plotly_events import plotly_events
# Suppress specific warnings
# warnings.filterwarnings("ignore", category=UserWarning, message="The widget with key.*")

st.set_page_config(page_title="Análisis Venta Global", layout="wide")

# Sample data for demonstration purposes


load_data()
# Layout for filters at the top

col1, col2, col3, col4 = st.columns(4)
col5, col6, col7, col8 = st.columns(4)

with col1:
    st.image('ZhonghuiTitle.png', width=320)

with col2:
    st.session_state['country_filter']  = set_expander_country(st.session_state.country_ls, st.session_state.country_ls)

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


# Filter the data based on selections
# filtered_data = data[
#     (data['Country'] == country_filter) &
#     ((data['Customer_Type'] == customer_type_filter) | (customer_type_filter == 'All')) &
#     (data['Category'].isin(category_filter)) &
#     ((data['Brand'] == brand_filter) | (brand_filter == 'All')) &
#     ((data['Product'] == product_filter) | (product_filter == 'All')) &
#     ((data['Seller'] == seller_filter) | (seller_filter == 'All')) 
#     (data['Date'] >= pd.to_datetime(date_range_filter[0])) &
#     (data['Date'] <= pd.to_datetime(date_range_filter[1]))
# ]

# Sample sales data
# Sample sales data


start_date = '2023-01-01'
end_date = '2023-12-31'


st.session_state['start_date'], st.session_state['end_date'] = set_date(start_date, end_date)

st.session_state['start_date_past'] = adjust_for_february(st.session_state['start_date'])
st.session_state['end_date_past'] = adjust_for_february(st.session_state['end_date'])

selected_df, selected_past_df = filter_data(st.session_state['country_filter'], st.session_state['product_filter'], st.session_state['brand_filter'], st.session_state['customer_type_filter'], st.session_state['seller_filter'], st.session_state['category_filter'], st.session_state['start_date_past'], st.session_state['start_date'], st.session_state['end_date'], st.session_state['end_date_past'])


build_tablet(selected_df, selected_past_df)

# Display the filtered data
# st.write("Filtered Data")
# st.write(filtered_data)

# Plotting the Sales over Time
# st.write("Sales Chart")
# if not filtered_data.empty:
#     filtered_data = filtered_data.sort_values(by='Date')
#     st.line_chart(filtered_data.set_index('Date')['Sales'])
# else:
#     st.write("No data available for the selected filters.")

plot_lineChart(selected_df, selected_past_df)


selected_customer_df = selected_df[['Customer Name', 'Amount']].groupby(['Customer Name']).sum()
selected_customer_past_df = selected_past_df[['Customer Name', 'Amount']].groupby(['Customer Name']).sum()
selected_customer_all_df =  selected_customer_df.merge(selected_customer_past_df, how="outer", on="Customer Name", suffixes=["_now", "_past"]).reset_index().rename({"Amount_now": "Ventas", "Amount_past":"Ventas Año Ant."}, axis=1)



plot_barChart(selected_customer_all_df)
# Sample Data similar to the provided image
# data = {
#     "Customer Name": ["NOGUERA Y VINTRO ANDALUCIA S.L", "SUMINISTROS DE OFICINAS ALCETONER, S.L",
#                 "SCOLARSON, S.L", "MUSTAFA AL LAL MAATEIS", "REGALOS DOMINGUEZ, S.L",
#                 "PALOMINO DEL PINO, HELIO ALEJANDRO", "NOVEDADES MARLU, S.L",
#                 "LEON TORRES, ALEJANDRO", "BAROPAPER, S.L", "RUEDA LÓPEZ, MAGDALENA",
#                 "RONDAN BAREA, JUAN FRANCISCO", "SICILIA BAUTISTA, NEMESIO",
#                 "SUMINISTROS DE PAPELERIA OFICASUR S.L", "RAMÓN PÉREZ, ROCÍO",
#                 "RUEDA LÓPEZ, MAGDALENA", "PEREZ-GIEB TORCIDA, JERONIMO"],
#     "Ventas": [5237, 4575, 3123, 2827, 2425, 2293, 1900, 432, 348, 235, 172, 165, 146, 27, 23, 0],
#     "Ventas Año Ant.": [3823, 2280, 2004, 1523, 1578, 2300, 1282, 818, 348, 235, 172, 148, 146, 27, 23, -35],
#     "Var Año-a-Año Ventas": [1414, 2295, 1119, 1304, 847, -7, 619, -386, 0, 0, 0, 17, 0, 0, 0, 35],
#     "% Var Año-a-Año Ventas": [37.00, 100.66, 55.86, 85.64, 53.68, -0.30, 48.28, -47.27, 0.00, 0.00, 0.00, 11.66, 0.00, 0.00, 0.00, 100.00]
# }

# df = pd.DataFrame(data)

# Streamlit Application
# st.title('Comparative Sales Analysis')

# # Table display toggle
# if st.checkbox("Show Data Table"):
#     st.dataframe(df)

# # Interactive Plotly Bar Chart
# fig = go.Figure()

# fig.add_trace(go.Bar(
#     y=df['Cliente'],
#     x=df['Ventas Año Ant.'],
#     name='Ventas Año Ant.',
#     orientation='h',
#     marker=dict(color='lightgrey')
# ))

# fig.add_trace(go.Bar(
#     y=df['Cliente'],
#     x=df['Var Año-a-Año Ventas'],
#     name='Var Año-a-Año Ventas',
#     orientation='h',
#     marker=dict(color='teal')
# ))

# fig.update_layout(
#     title='Ventas Año-a-Año Comparativo',
#     xaxis_title='Euros',
#     yaxis_title='Clientes',
#     barmode='stack',
#     legend=dict(x=0.5, y=1.1, orientation='h'),
#     margin=dict(l=150, r=10, t=70, b=70)
# )

# st.plotly_chart(fig)



###################################################

# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go

# Sample Data similar to the provided image
# data = {
#     "Customer Name": [
#         "NOGUERA Y VINTRO ANDALUCIA S.L", "SUMINISTROS DE OFICINAS ALCETONER, S.L",
#         "SCOLARSON, S.L", "MUSTAFA AL LAL MAATEIS", "REGALOS DOMINGUEZ, S.L",
#         "PALOMINO DEL PINO, HELIO ALEJANDRO", "NOVEDADES MARLU, S.L",
#         "LEON TORRES, ALEJANDRO", "BAROPAPER, S.L", "RUEDA LÓPEZ, MAGDALENA",
#         "RONDAN BAREA, JUAN FRANCISCO", "SICILIA BAUTISTA, NEMESIO",
#         "SUMINISTROS DE PAPELERIA OFICASUR S.L", "RAMÓN PÉREZ, ROCÍO",
#         "RUEDA LÓPEZ, MAGDALENA", "PEREZ-GIEB TORCIDA, JERONIMO"
#     ],
#     "Ventas": [5237, 4575, 3123, 2827, 2425, 2293, 1900, 432, 348, 235, 172, 165, 146, 27, 23, 0],
#     "Ventas Año Ant.": [3823, 2280, 2004, 1523, 1578, 2300, 1282, 818, 348, 235, 172, 148, 146, 27, 23, -35],
#     "Var pos Año-a-Año Ventas": [1414, 2295, 1119, 1304, 847, 0, 619, 0, 0, 0, 0, 17, 0, 0, 0, 35],
#     "Var neg Año-a-Año Ventas": [0, 0, 0, 0, 0, -7, 0, -386, 0, 0, 0, 0, 0, 0, 0, 0],
#     "% Var Año-a-Año Ventas": [37.00, 100.66, 55.86, 85.64, 53.68, -0.30, 48.28, -47.27, 0.00, 0.00, 0.00, 11.66, 0.00, 0.00, 0.00, 100.00]
# }

# selected_customer_all_df = pd.DataFrame(data)




# country_map_df = pd.read_csv("data/country_map.csv", index_col=0)
# country_map = country_map_df.drop(["3-Digit Code"], axis=1).set_index("2-Digit Code").squeeze().to_dict()
# map_df = selected_df.groupby(['Sell-to Country_Region Code'])['Amount'].sum().reset_index()
# map_df['Country'] = map_df['Sell-to Country_Region Code'].map(country_map)
# map_df = map_df.drop(['Sell-to Country_Region Code'], axis=1).rename({"Amount": "Sales"}, axis=1)


# # Sample sales data for various locations (You can replace this with your own data)
# # data = {
# #     'Country': ['United States', 'Canada', 'Brazil', 'India', 'China', 'Australia', 'Russia'],
# #     'Sales': [200000, 180000, 150000, 170000, 130000, 140000, 120000]
# # }

# # # Create a DataFrame
# # df = pd.DataFrame(data)

# # Load world countries shapefile
# # Using a GeoJSON file for the world's countries for convenience
# shapefile_path = gpd.datasets.get_path('naturalearth_lowres')
# gdf_countries = gpd.read_file(shapefile_path)

# # Merge sales data with countries GeoDataFrame
# gdf_countries = gdf_countries.merge(map_df, left_on='name', right_on='Country', how='left')


# # Streamlit app
# st.title('Global Sales Geomap')

# st.markdown("""
# This app visualizes sales data for various countries. The color intensity of each country corresponds to the sales volume at that location.
# """)

# sales_max = map_df['Sales'].max()
# # Create a folium map
# m = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodb positron')

# # Define a function to style the GeoJson based on sales
# def style_function(feature):
#     sales = feature['properties']['Sales']
#     return {
#         'fillOpacity': 0.7,
#         'weight': 0.5,
#         'fillColor': '#808080'  if sales is None else '#%02x%02x%02x' % (int(np.log(sales) / np.log(sales_max) * 255), 0, 255 - int(np.log(sales) / np.log(sales_max) * 255))
#     }

# # Add the GeoJson layer to the map
# folium.GeoJson(
#     gdf_countries,
#     style_function=style_function,
#     tooltip=GeoJsonTooltip(fields=['name', 'Sales'], aliases=['Country', 'Sales'], localize=True)
# ).add_to(m)

# # Save the map to an HTML file
# m.save('map.html')

# # Display the map in Streamlit
# st.components.v1.html(m._repr_html_(), width=1400, height=800)

# # Optional: Dynamic data input (e.g., user uploads CSV)
# st.sidebar.title("Upload Sales Data")
# uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv"])
# if uploaded_file is not None:
#     user_data = pd.read_csv(uploaded_file)
#     gdf_countries = gdf_countries.merge(user_data, left_on='name', right_on='Country', how='left')

#     # Create a new folium map with user data
#     m_user = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodb positron')

#     # Add the GeoJson layer to the map with user data
#     folium.GeoJson(
#         gdf_countries,
#         style_function=style_function,
#         tooltip=GeoJsonTooltip(fields=['name', 'Sales'], aliases=['Country', 'Sales'], localize=True)
#     ).add_to(m_user)

#     # Save the map to an HTML file
#     m_user.save('user_map.html')

#     # Display the map in Streamlit
#     st.components.v1.html(m_user._repr_html_(), width=1400, height=800)

#######################################################################################





import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip, GeoJsonPopup
import numpy as np

# Sample sales data for various locations (Replace with your actual data)
# Load your country map and sales data
country_map_df = pd.read_csv("data/country_map.csv", index_col=0)
country_map = country_map_df.drop(["3-Digit Code"], axis=1).set_index("2-Digit Code").squeeze().to_dict()
# selected_df = pd.read_csv("data/sales_data.csv")  # Replace with actual sales data CSV path
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
        'fillColor': '#808080' if sales is None else '#%02x%02x%02x' % (int(np.log(sales) / np.log(sales_max) * 255), 0, 255 - int(np.log(sales) / np.log(sales_max) * 255))
    }

# Add the GeoJson layer to the map
geojson = folium.GeoJson(
    gdf_countries,
    style_function=style_function,
    tooltip=GeoJsonTooltip(fields=['name', 'Sales'], aliases=['Country', 'Sales'], localize=True)
).add_to(m)

# Add click event to the GeoJson layer
# Add click event to the GeoJson layer
# geojson.add_child(folium.features.GeoJsonPopup(fields=['name'], aliases=['Country'], labels=False, style="font-size: 12px;"))

# # JavaScript for capturing click events and sending the data back to Streamlit
# click_js = """
# <script>
#     function onMapClick(e) {
#         var layer = e.layer;
#         if (layer.feature) {
#             var country = layer.feature.properties.name;
#             window.parent.postMessage({ type: 'country', country: country }, '*');
#         }
#     }
#     document.querySelectorAll('.folium-map')[0].style.height = '600px';
#     document.querySelectorAll('.folium-map')[0].style.width = '100%';
#     var map = document.querySelectorAll('.folium-map')[0].__folium;
#     map.on('click', onMapClick);
# </script>
# """

# Save the map to an HTML file
m.save('map.html')

# Display the map in Streamlit
st.components.v1.html(m._repr_html_(), width=1400, height=800)


# # JavaScript to handle the message and update the Streamlit session state
# session_js = """
# <script>
#     window.addEventListener("message", (event) => {
#         if (event.data.type && event.data.type === 'country') {
#             const country = event.data.country;
#             window.parent.postMessage({ type: 'update', country: country }, '*');
#         }
#     });
# </script>
# """

# # Hidden text input to store the country value
# hidden_input = """
# <input type="hidden" id="country-input" />
# """

# # Display the hidden input and JavaScript
# html(hidden_input + session_js, height=0, width=0)

# # Initialize session state
# if 'country' not in st.session_state:
#     st.session_state['country'] = ''

# # Function to update session state
# def update_country():
#     js_code = """
#     <script>
#         const input = document.getElementById('country-input');
#         input.addEventListener('input', function() {
#             const country = input.value;
#             window.parent.postMessage({ type: 'update', country: country }, '*');
#         });
#     </script>
#     """
#     html(js_code, height=0, width=0)

# # Call function to ensure session state updates
# update_country()

# # JavaScript to capture the updated country value
# st.components.v1.html("""
# <script>
#     window.addEventListener("message", (event) => {
#         if (event.data.type && event.data.type === 'update') {
#             const country = event.data.country;
#             const input = document.getElementById('country-input');
#             if (input) {
#                 input.value = country;
#                 input.dispatchEvent(new Event('input', { bubbles: true }));
#             }
#         }
#     });
# </script>
# """, height=0, width=0)

# # Display the clicked country in Streamlit
# if st.session_state['country']:
#     st.write(f"You clicked on: {st.session_state['country']}")