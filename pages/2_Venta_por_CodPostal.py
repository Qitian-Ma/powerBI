
# import pandas as pd
# import streamlit as st
# from st_aggrid import AgGrid, GridOptionsBuilder
# from st_aggrid.shared import GridUpdateMode




# def aggrid_interactive_table(df: pd.DataFrame):
#     """Creates an st-aggrid interactive table based on a dataframe.

#     Args:
#         df (pd.DataFrame]): Source dataframe

#     Returns:
#         dict: The selected row
#     """
#     options = GridOptionsBuilder.from_dataframe(
#         df, enableRowGroup=True, enableValue=True, enablePivot=True, resizable=True,  filterable=True, groupable=True
#     )

#     options.configure_side_bar()

#     options.configure_selection("single")
#     selection = AgGrid(
#         df,
#         enable_enterprise_modules=True,
#         gridOptions=options.build(),
#         theme="material",
#         update_mode=GridUpdateMode.MODEL_CHANGED,
#         allow_unsafe_jscode=True,
#     )

#     return selection


# iris = pd.read_csv(
#     "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
# )

# selection = aggrid_interactive_table(df=iris)

# if selection:
#     st.write("You selected:")
#     st.write(selection["selected_rows"])

# import pandas as pd
# import streamlit as st
# from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
# from st_aggrid.shared import GridUpdateMode

# # Function to render progress bar as HTML
# def render_progress_bar(sales):
#     color = "green" if sales >= 0 else "red"
#     percentage = abs(sales)
#     if sales >= 0:
#         return (
#             f'<div style="width: 300px; background-color: #e0e0e0; border-radius: 5px; position: relative; height: 20px;">'
#             f'<div style="width: {percentage}%; background-color: {color}; height: 100%; border-radius: 5px; position: absolute; top: 0; left: 50%; transform: translateX(0%);">'
#             f'</div>'
#             f'</div>'
#         ).replace('\n', '')
#     else:
#         return (
#             f'<div style="width: 300px; background-color: #e0e0e0; border-radius: 5px; position: relative; height: 20px;">'
#             f'<div style="width: {percentage}%; background-color: {color}; height: 100%; border-radius: 5px; position: absolute; top: 0; right: 50%; transform: translateX(-100%);">'
#             f'</div>'
#             f'</div>'
#         ).replace('\n', '')



# # Add a progress column to the iris DataFrame
# iris = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv")
# iris['progress'] = iris['sepal_length'].apply(render_progress_bar)

# # Function to create an interactive table with AgGrid
# def aggrid_interactive_table(df: pd.DataFrame):
#     options = GridOptionsBuilder.from_dataframe(
#         df, enableRowGroup=True, enableValue=True, enablePivot=True, resizable=True, filterable=True, groupable=True, editable=True
#     )

#     options.configure_side_bar()
#     options.configure_selection("single")

#     # Add custom cell renderer for the progress column
#     cell_renderer = JsCode("""
#     class HtmlRenderer {
#         init(params) {
#             this.eGui = document.createElement('div');
#             this.eGui.innerHTML = params.value;
#         }
#         getGui() {
#             return this.eGui;
#         }
#     }
#     """)

#     options.configure_column("progress", header_name="Progress", cellRenderer=cell_renderer)
    
#     selection = AgGrid(
#         df,
#         enable_enterprise_modules=True,
#         gridOptions=options.build(),
#         theme="material",
#         update_mode=GridUpdateMode.MODEL_CHANGED,
#         allow_unsafe_jscode=True,
#     )

#     return selection

# # Render the interactive table
# selection = aggrid_interactive_table(df=iris)

# # Display selected rows
# if selection:
#     st.write("You selected:")
#     st.write(selection["selected_rows"])

# import pandas as pd
# import streamlit as st
# from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
# from st_aggrid.shared import GridUpdateMode

# # Sample sales data for this year and last year
# data = {
#     'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
#     'This Year': [120, 100, 300, 400, 500],
#     'Last Year': [100, 250, 150, 300, 450]
# }

# sales_df = pd.DataFrame(data)

# # Function to calculate year-to-year percentage difference and render progress bar
# def render_progress_bar(row):
#     this_year = row['This Year']
#     last_year = row['Last Year']
#     if last_year != 0:
#         percentage_diff = ((this_year - last_year) / abs(last_year)) * 100
#     else:
#         percentage_diff = 0  # Avoid division by zero

#     # color = "green" if percentage_diff >= 0 else "red"
#     # percentage = abs(percentage_diff)
#     # direction = "left" if percentage_diff >= 0 else "right"
#     # text_position = "right" if percentage_diff >= 0 else "left"
#     color = "green" if percentage_diff >= 0 else "red"
#     if percentage_diff >= 0:
#         return (
#             f'<div style="width: 100px; background-color: #e0e0e0; border-radius: 5px; position: absolute; height: 20px; top: 25%">'
#             f'<div style="width: {percentage_diff / 2}%; background-color: {color}; height: 100%; border-radius: 5px; position: absolute; top: 0; left: 50%; transform: translateX(0%);">'
#             f'</div>'
#             f'</div>'
#         ).replace('\n', '')
#     else:
#         return (
#             f'<div style="width: 100px; background-color: #e0e0e0; border-radius: 5px; position: absolute; height: 20px; top: 25%">'
#             f'<div style="width: {-percentage_diff / 2}%; background-color: {color}; height: 100%; border-radius: 5px; position: absolute; top: 0; right: 50%; transform: translateX(0%);">'
#             f'</div>'
#             f'</div>'
#         ).replace('\n', '')

# # Add a progress column to the sales DataFrame
# sales_df['Progress'] = sales_df.apply(render_progress_bar, axis=1)

# # Function to create an interactive table with AgGrid
# def aggrid_interactive_table(df: pd.DataFrame):
#     options = GridOptionsBuilder.from_dataframe(
#         df, enableRowGroup=True, enableValue=True, enablePivot=True, resizable=True, filterable=True, groupable=True, selection_mode='multiple'
#     )

#     options.configure_side_bar()
#     options.configure_selection("single")

#     # Add custom cell renderer for the progress column
#     cell_renderer = JsCode("""
#     class HtmlRenderer {
#         init(params) {
#             this.eGui = document.createElement('div');
#             this.eGui.innerHTML = params.value;
#         }
#         getGui() {
#             return this.eGui;
#         }
#     }
#     """)

#     options.configure_column("Progress", header_name="Progress", cellRenderer=cell_renderer)
    
#     selection = AgGrid(
#         df,
#         enable_enterprise_modules=True,
#         gridOptions=options.build(),
#         theme="material",
#         update_mode=GridUpdateMode.MODEL_CHANGED,
#         allow_unsafe_jscode=True,
#     )

#     return selection

# # Render the interactive table
# selection = aggrid_interactive_table(df=sales_df)

# # Display selected rows
# if selection:
#     st.write("You selected:")
#     st.write(selection["selected_rows"])

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MousePosition
import folium as fl
from streamlit_folium import st_folium

# Load postal code data with sales
postal_codes = {
    "PostalCode": ["28001", "08001", "46001", "41001", "35001", "29001", "48001", "33001", "20001", "24001"],
    "City": ["Madrid", "Barcelona", "Valencia", "Seville", "Las Palmas", "Malaga", "Bilbao", "Oviedo", "San Sebastian", "Leon"],
    "Latitude": [40.4218, 41.3809, 39.4713, 37.3886, 28.1235, 36.7213, 43.2627, 43.3603, 43.3224, 42.5992],
    "Longitude": [-3.6856, 2.1756, -0.3764, -5.9823, -15.4314, -4.4214, -2.9350, -5.8448, -1.9860, -5.5704],
    "Sales": [3069, 2045, 4616, 9231, 2014, 8579, 7807, 2792, 9313, 1193]
}

df = pd.DataFrame(postal_codes)
def get_pos(lat,lng):
    return lat,lng

# Create a map centered around Spain
m = folium.Map(location=[40.0, -3.7], zoom_start=6)
m.add_child(fl.LatLngPopup())
MousePosition().add_to(m)
# Add points to the map with sales data
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Sales'] / 1000,  # Adjust the radius based on sales
        popup=f"{row['City']} ({row['PostalCode']}): {row['Sales']} sales",
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

map2 = st_folium(m, height=350, width=700)
data = get_pos(map2['last_clicked']['lat'],map2['last_clicked']['lng'])

if data is not None:
    st.write(data)

# Display the map
# folium_static(m)

from opencage.geocoder import OpenCageGeocode

def get_postal_code(lat, lon, api_key):
    """
    This function takes latitude, longitude, and an OpenCage API key as inputs and returns the corresponding Spanish postal code.
    
    :param lat: Latitude
    :param lon: Longitude
    :param api_key: OpenCage API key
    :return: Postal code
    """
    geocoder = OpenCageGeocode(api_key)

    try:
        results = geocoder.reverse_geocode(lat, lon, language='es')
        if results and 'postcode' in results[0]['components']:
            return results[0]['components']['postcode']
        else:
            return "Postal code not found"
    except Exception as e:
        return f"Error: {e}"

# Example usage
api_key = 'lbKHwnrO08h3PTlavGwXa5_9nqX6eiInwi7ZF9qw8wQ'  # Replace with your OpenCage API key
lat = 40.4218
lon = -3.6856
postal_code = get_postal_code(lat, lon, api_key)
st.write(f"The postal code for coordinates ({lat}, {lon}) is {postal_code}")

# https://www.here.com/docs/bundle/geocoding-and-search-api-developer-guide/page/topics/quick-start.html