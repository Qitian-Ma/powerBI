import streamlit as st
import pandas as pd
from dask.dataframe import from_pandas
import dask.dataframe as dd
import numpy as np
from tablet import get_html, custom_css

import warnings


# Suppress specific warnings
# warnings.filterwarnings("ignore", category=UserWarning, message="The widget with key.*")

st.set_page_config(page_title="Análisis Venta Global", layout="wide")
st.write("Dask")
# Sample data for demonstration purposes
@st.cache_data
def load_sales_data():
    salesLine_df = dd.read_csv(r"data\salesLine_2324.csv")
    salesHeader_df = dd.read_csv(r"data\salesHeader_2324.csv")
    return salesHeader_df, salesLine_df

@st.cache_data
def load_customer_data():
    customer_df = dd.read_csv(r"data\customer.csv")
    return customer_df

@st.cache_data
def load_dimension_data():
    dimension_df = dd.read_csv(r"data\dimension.csv")
    return dimension_df

@st.cache_data
def load_classification_data():
    productGroup_df = dd.read_csv(r"data\productGroup.csv")
    itemCategory_df = dd.read_csv(r"data\itemCategory.csv")
    return productGroup_df, itemCategory_df

@st.cache_data
def load_salesPerson_data():
    salesPerson_df = dd.read_csv(r"data\salesPerson.csv")
    return salesPerson_df

salesHeader_df, salesLine_df = load_sales_data()
customer_df = load_customer_data()
dimension_df = load_dimension_data()
productGroup_df, itemCategory_df = load_classification_data()
salesPerson_df = load_salesPerson_data()

st.write(salesHeader_df.head())
def convert_to_datetime(df):
    df['Posting Date'] = dd.to_datetime(df['Posting Date'], format='%Y-%m-%d')
    return df
salesHeader_df['Posting Date'] = salesHeader_df['Posting Date'].map_partitions(convert_to_datetime,  meta={'Posting Date': 'datetime64[ns]'}).compute()


# salesHeader_df['Sell-to Country_Region Code'] = salesHeader_df['Sell-to Country_Region Code'].fillna(salesHeader_df['Bill-to Country_Region Code']).fillna(salesHeader_df['VAT Country_Region Code']).fillna(salesHeader_df["Ship-to Country_Region Code"])
# salesHeader_df['Sell-to County'] = salesHeader_df['Sell-to County'].fillna(salesHeader_df['Bill-to County']).fillna(salesHeader_df['Ship-to County'])
# salesHeader_df['Sell-to Post Code'] = salesHeader_df['Sell-to Post Code'].fillna(salesHeader_df['Bill-to Post Code']).fillna(salesHeader_df['Ship-to Post Code'])

# salesHeader_df.drop(['Bill-to Country_Region Code', 'VAT Country_Region Code', 'Bill-to County', 'Bill-to Post Code', "Ship-to Country_Region Code", 'Ship-to County', 'Ship-to Post Code'], axis=1, inplace=True)



# Layout for filters at the top

col1, col2, col3, col4 = st.columns(4)
col5, col6, col7, col8 = st.columns(4)

with col1:
    st.image('ZhonghuiTitle.png', width=320)

def clear_settings_country():
    st.session_state.selected_options_country = []

def clear_settings_client():
    st.session_state.selected_options_client = []

def clear_settings_category():
    st.session_state.selected_options_category = []

def clear_settings_brand():
    st.session_state.selected_options_brand = []

def clear_settings_product():
    st.session_state.selected_options_product = []

def clear_settings_seller():
    st.session_state.selected_options_seller = []

def select_all_country():
    st.session_state.selected_options_country = ['ES', 'IT']

def select_all_client():
    st.session_state.selected_options_client = dimension_df['Dimension Name'].unique().tolist()

def select_all_category():
    st.session_state.selected_options_category = itemCategory_df['Item Category Description'].unique().tolist()

def select_all_brand():
    st.session_state.selected_options_brand = salesLine_df['Brand Code'].dropna().unique().tolist()

def select_all_product():
    st.session_state.selected_options_product = salesLine_df['Product No_'].unique().tolist()

def select_all_seller():   
    st.session_state.selected_options_seller = salesPerson_df['Salesperson Name'].unique().tolist()

with col2:
    with st.expander("País"):
        col21, col22 = st.columns(2)
        with col21:
            st.button('Clear Selections', on_click=clear_settings_country, key='21')
        with col22:
            st.button('Select All', on_click=select_all_country, key='22', type="primary", use_container_width=True)
        country_filter = st.multiselect('País', default=['ES'], options=['ES', 'IT'], label_visibility ="collapsed", key='selected_options_country')
        
            

with col3:
    with st.expander("Tipo Cliente"):
        col31, col32 = st.columns(2)
        with col31:
            st.button('Clear Selections', on_click=clear_settings_client, key='31')
        with col32:
            st.button('Select All', on_click=select_all_client, key='32', type="primary", use_container_width=True)
        customer_type_filter = st.multiselect('Tipo Cliente', default=dimension_df['Dimension Name'].unique().tolist(), options=dimension_df['Dimension Name'].unique().tolist(), label_visibility ="collapsed", key='selected_options_client')
        

with col4:
    with st.expander("Categoría, Subcategoría"):
        col41, col42 = st.columns(2)
        with col41:
            st.button('Clear Selections', on_click=clear_settings_category, key='41')
        with col42:
            st.button('Select All', on_click=select_all_category, key='42', type="primary", use_container_width=True)
        category_filter = st.multiselect('Categoría, Subcategoría', default=itemCategory_df['Item Category Description'].unique().tolist(), options=itemCategory_df['Item Category Description'].unique().tolist(), label_visibility ="collapsed", key='selected_options_category')
        

with col5:
    st.markdown('<h3 class="custom-header", style="text-align: center;">Análisis Venta Global</h3>', unsafe_allow_html=True)

with col6:
    with st.expander("Marca"):
        col61, col62 = st.columns(2)
        with col61:
            st.button('Clear Selections', on_click=clear_settings_brand, key='61')
        with col62:
            st.button('Select All', on_click=select_all_brand, key='62', type="primary", use_container_width=True)
        brand_filter = st.multiselect('Marca', default=salesLine_df['Brand Code'].dropna().unique().tolist(), options=salesLine_df['Brand Code'].dropna().unique().tolist(), label_visibility ="collapsed", key='selected_options_brand')
        
with col7:
    with st.expander("Producto"):
        col71, col72 = st.columns(2)
        with col71:
            st.button('Clear Selections', on_click=clear_settings_product, key='71')
        with col72:
            st.button('Select All', on_click=select_all_product, key='72', type="primary", use_container_width=True)
        product_filter = st.multiselect('Producto', default=salesLine_df['Product No_'].unique().tolist(), options=salesLine_df['Product No_'].unique().tolist(), label_visibility ="collapsed", key='selected_options_product')

with col8:
    with st.expander("Vendedor"):
        col81, col82 = st.columns(2)
        with col81:
            st.button('Clear Selections', on_click=clear_settings_seller, key='81')
        with col82:
            st.button('Select All', on_click=select_all_seller, key='82', type="primary", use_container_width=True)
        seller_filter = st.multiselect('Vendedor', default=salesPerson_df['Salesperson Name'].unique().tolist(), options=salesPerson_df['Salesperson Name'].unique().tolist(), label_visibility ="collapsed", key='selected_options_seller')

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

col14, col15, col16 = st.columns([1, 1, 6])

with col14:
    if 'start_date' not in st.session_state:
        start_date = st.date_input('Start date', pd.to_datetime('2023-01-01'))
        st.session_state['start_date'] = start_date
    else:
        start_date = st.date_input('Start date', st.session_state['start_date'])


with col15:
    if 'end_date' not in st.session_state:
        end_date = st.date_input('End date', pd.to_datetime('2023-12-31'))
        st.session_state['end_date'] = end_date
    else:
        end_date = st.date_input('End date', st.session_state['end_date'])

# start_date = datetime.date(2022, 4, 30)
# end_date = datetime.date(2024, 6, 6)


with col16:
    date_range = st.slider('Fecha', min_value=pd.to_datetime('2023-01-01'), max_value=pd.to_datetime('2023-12-31'), value=(pd.Timestamp(start_date).to_pydatetime(), pd.Timestamp(end_date).to_pydatetime()), format="YYYY-MM-DD")
    start_date = date_range[0]
    end_date = date_range[1]
    if start_date != st.session_state.start_date or end_date != st.session_state.end_date:
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        st.experimental_rerun()


salesHeader_selected_df = salesHeader_df[(salesHeader_df['Posting Date'] >= pd.to_datetime(start_date)) & (salesHeader_df['Posting Date'] <= pd.to_datetime(end_date)) & 
                                         (salesHeader_df['Sell-to Country_Region Code'].isin(country_filter)) ] 
salesLine_selected_df = salesLine_df[(salesLine_df['Product No_'].isin(product_filter)) & salesLine_df['Brand Code'].isin(brand_filter)]
dimension_selected_df = dimension_df[dimension_df['Dimension Name'].isin(customer_type_filter)]
salesPerson_selected_df = salesPerson_df[salesPerson_df['Salesperson Name'].isin(seller_filter)]
itemCategory_selected_df = itemCategory_df[itemCategory_df['Item Category Description'].isin(category_filter)]



selected_df = dimension_selected_df.merge(customer_df, how='inner', left_on='Dimension Code', right_on='Global Dimension 1 Code')\
.merge(salesHeader_selected_df, how='inner', left_on='Customer No_', right_on="Sell-to Customer No_")\
.merge(salesPerson_selected_df, how='inner', left_on='Salesperson Code', right_on='Salesperson Code')\
.merge(salesLine_selected_df, how='inner', left_on='Document No_', right_on='Document No_')\
.merge(itemCategory_selected_df , how='inner', left_on='Item Category Code', right_on='Item Category Code')

st.write(selected_df.head())
st.write(selected_df.shape)



col9, col10, col11, col12, col13 = st.columns(5, gap='large')

with col9:
    current_sales = 14070
    previous_sales = 19498
    diff_percentage = ((current_sales - previous_sales) / previous_sales) * 100

    st.markdown(custom_css, unsafe_allow_html=True)

    sales_widget_html = get_html("Ventas", current_sales, previous_sales, diff_percentage)

    st.markdown(sales_widget_html, unsafe_allow_html=True)

with col10:
    current_sales = 139
    previous_sales = 90
    diff_percentage = ((current_sales - previous_sales) / previous_sales) * 100

    st.markdown(custom_css, unsafe_allow_html=True)

    sales_widget_html = get_html("No. Facturas", current_sales, previous_sales, diff_percentage)

    st.markdown(sales_widget_html, unsafe_allow_html=True)


with col11:
    current_sales = 172
    previous_sales = 185
    diff_percentage = ((current_sales - previous_sales) / previous_sales) * 100

    st.markdown(custom_css, unsafe_allow_html=True)

    sales_widget_html = get_html("Ticket Medio", current_sales, previous_sales, diff_percentage)

    st.markdown(sales_widget_html, unsafe_allow_html=True)


with col12:
    current_sales = 18535
    previous_sales = 13597
    diff_percentage = ((current_sales - previous_sales) / previous_sales) * 100

    st.markdown(custom_css, unsafe_allow_html=True)

    sales_widget_html = get_html("No. Unidades", current_sales, previous_sales, diff_percentage)

    st.markdown(sales_widget_html, unsafe_allow_html=True)

with col13:
    current_sales = 120
    previous_sales = 95
    diff_percentage = ((current_sales - previous_sales) / previous_sales) * 100

    st.markdown(custom_css, unsafe_allow_html=True)

    sales_widget_html = get_html("No. Artículos Distintos", current_sales, previous_sales, diff_percentage)

    st.markdown(sales_widget_html, unsafe_allow_html=True)


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


datasets = pd.DataFrame.from_dict({"a": list(range(100)), "b": list(np.random.randint(0, 100, 100)), "c": list(np.random.randint(0, 100, 100))})
st.area_chart(
    data=datasets,
    x='a',
    y=['b', 'c'],
    color=["#619CFF", "#F8766D"])

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Sample Data similar to the provided image
data = {
    "Cliente": ["NOGUERA Y VINTRO ANDALUCIA S.L", "SUMINISTROS DE OFICINAS ALCETONER, S.L",
                "SCOLARSON, S.L", "MUSTAFA AL LAL MAATEIS", "REGALOS DOMINGUEZ, S.L",
                "PALOMINO DEL PINO, HELIO ALEJANDRO", "NOVEDADES MARLU, S.L",
                "LEON TORRES, ALEJANDRO", "BAROPAPER, S.L", "RUEDA LÓPEZ, MAGDALENA",
                "RONDAN BAREA, JUAN FRANCISCO", "SICILIA BAUTISTA, NEMESIO",
                "SUMINISTROS DE PAPELERIA OFICASUR S.L", "RAMÓN PÉREZ, ROCÍO",
                "RUEDA LÓPEZ, MAGDALENA", "PEREZ-GIEB TORCIDA, JERONIMO"],
    "Ventas": [5237, 4575, 3123, 2827, 2425, 2293, 1900, 432, 348, 235, 172, 165, 146, 27, 23, 0],
    "Ventas Año Ant.": [3823, 2280, 2004, 1523, 1578, 2300, 1282, 818, 348, 235, 172, 148, 146, 27, 23, -35],
    "Var Año-a-Año Ventas": [1414, 2295, 1119, 1304, 847, -7, 619, -386, 0, 0, 0, 17, 0, 0, 0, 35],
    "% Var Año-a-Año Ventas": [37.00, 100.66, 55.86, 85.64, 53.68, -0.30, 48.28, -47.27, 0.00, 0.00, 0.00, 11.66, 0.00, 0.00, 0.00, 100.00]
}

df = pd.DataFrame(data)

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

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Sample Data similar to the provided image
data = {
    "Cliente": [
        "NOGUERA Y VINTRO ANDALUCIA S.L", "SUMINISTROS DE OFICINAS ALCETONER, S.L",
        "SCOLARSON, S.L", "MUSTAFA AL LAL MAATEIS", "REGALOS DOMINGUEZ, S.L",
        "PALOMINO DEL PINO, HELIO ALEJANDRO", "NOVEDADES MARLU, S.L",
        "LEON TORRES, ALEJANDRO", "BAROPAPER, S.L", "RUEDA LÓPEZ, MAGDALENA",
        "RONDAN BAREA, JUAN FRANCISCO", "SICILIA BAUTISTA, NEMESIO",
        "SUMINISTROS DE PAPELERIA OFICASUR S.L", "RAMÓN PÉREZ, ROCÍO",
        "RUEDA LÓPEZ, MAGDALENA", "PEREZ-GIEB TORCIDA, JERONIMO"
    ],
    "Ventas": [5237, 4575, 3123, 2827, 2425, 2293, 1900, 432, 348, 235, 172, 165, 146, 27, 23, 0],
    "Ventas Año Ant.": [3823, 2280, 2004, 1523, 1578, 2300, 1282, 818, 348, 235, 172, 148, 146, 27, 23, -35],
    "Var pos Año-a-Año Ventas": [1414, 2295, 1119, 1304, 847, 0, 619, 0, 0, 0, 0, 17, 0, 0, 0, 35],
    "Var neg Año-a-Año Ventas": [0, 0, 0, 0, 0, -7, 0, -386, 0, 0, 0, 0, 0, 0, 0, 0],
    "% Var Año-a-Año Ventas": [37.00, 100.66, 55.86, 85.64, 53.68, -0.30, 48.28, -47.27, 0.00, 0.00, 0.00, 11.66, 0.00, 0.00, 0.00, 100.00]
}

df = pd.DataFrame(data)

# Streamlit Application
st.title('Comparative Sales Analysis')

# Table display toggle
if st.checkbox("Show Data Table"):
    st.dataframe(df)

# Filters for interactivity
selected_clients = st.multiselect(
    'Select Clients', options=df['Cliente'], default=df['Cliente']
)

# Filter data based on selection
filtered_df = df[df['Cliente'].isin(selected_clients)]

# Interactive Plotly Bar Chart
fig = go.Figure()



fig.add_trace(go.Bar(
    y=filtered_df['Cliente'],
    x=filtered_df['Ventas Año Ant.'],
    name='Ventas Año Ant.',
    orientation='h',
    marker=dict(color='lightgrey')
))

fig.add_trace(go.Bar(
    y=filtered_df['Cliente'],
    x=filtered_df['Var pos Año-a-Año Ventas'],
    name='Var pos Año-a-Año Ventas',
    orientation='h',
    marker=dict(color='rgb(255,72,105)')
))

fig.add_trace(go.Bar(
    y=filtered_df['Cliente'],
    x=filtered_df['Var neg Año-a-Año Ventas'],
    name='Var neg Año-a-Año Ventas',
    orientation='h',
    marker=dict(color='rgb(0, 183, 150)')
))

# Adding percentage change as text on the bars
for idx, row in filtered_df.iterrows():
    fig.add_annotation(
        x=row['Ventas Año Ant.'] + (row['Var pos Año-a-Año Ventas'] / 2) if row['Var pos Año-a-Año Ventas'] > 0 else row['Ventas Año Ant.'] + (row['Var neg Año-a-Año Ventas'] / 2) ,
        y=idx,
        text=f"{row['% Var Año-a-Año Ventas']}%",
        showarrow=False,
        font=dict(size=10, color="black")
    )

for idx, row in filtered_df.iterrows():
    fig.add_annotation(
        x=row['Ventas']  + 200 if row['Var pos Año-a-Año Ventas'] > 0 else row['Ventas Año Ant.'] + 200,
        y=idx,
        text=f"{row['Ventas']}",
        showarrow=False,
        font=dict(size=10, color="black")
    )


fig.update_layout(
    title='Ventas Año-a-Año Comparativo',
    xaxis_title='Euros',
    yaxis_title='Clientes',
    barmode='stack',
    legend=dict(x=0.5, y=1.1, orientation='h'),
    margin=dict(l=150, r=10, t=70, b=70),
    height=600,
    width=1500
)

st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJson, GeoJsonTooltip

# Sample sales data for various locations (You can replace this with your own data)
data = {
    'Country': ['United States', 'Canada', 'Brazil', 'India', 'China', 'Australia', 'Russia'],
    'Sales': [200000, 180000, 150000, 170000, 130000, 140000, 120000]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Load world countries shapefile
# Using a GeoJSON file for the world's countries for convenience
shapefile_path = gpd.datasets.get_path('naturalearth_lowres')
gdf_countries = gpd.read_file(shapefile_path)

# Merge sales data with countries GeoDataFrame
gdf_countries = gdf_countries.merge(df, left_on='name', right_on='Country', how='left')

# Streamlit app
st.title('Global Sales Geomap')

st.markdown("""
This app visualizes sales data for various countries. The color intensity of each country corresponds to the sales volume at that location.
""")

# Create a folium map
m = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodb positron')

# Define a function to style the GeoJson based on sales
def style_function(feature):
    sales = feature['properties']['Sales']
    return {
        'fillOpacity': 0.7,
        'weight': 0.5,
        'fillColor': '#ff0000' if sales is None else '#%02x%02x%02x' % (255 - int(sales / 200000 * 255), 0, int(sales / 200000 * 255))
    }

# Add the GeoJson layer to the map
folium.GeoJson(
    gdf_countries,
    style_function=style_function,
    tooltip=GeoJsonTooltip(fields=['name', 'Sales'], aliases=['Country', 'Sales'], localize=True)
).add_to(m)

# Save the map to an HTML file
m.save('map.html')

# Display the map in Streamlit
st.components.v1.html(m._repr_html_(), width=1400, height=800)

# Optional: Dynamic data input (e.g., user uploads CSV)
st.sidebar.title("Upload Sales Data")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv"])
if uploaded_file is not None:
    user_data = pd.read_csv(uploaded_file)
    gdf_countries = gdf_countries.merge(user_data, left_on='name', right_on='Country', how='left')

    # Create a new folium map with user data
    m_user = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodb positron')

    # Add the GeoJson layer to the map with user data
    folium.GeoJson(
        gdf_countries,
        style_function=style_function,
        tooltip=GeoJsonTooltip(fields=['name', 'Sales'], aliases=['Country', 'Sales'], localize=True)
    ).add_to(m_user)

    # Save the map to an HTML file
    m_user.save('user_map.html')

    # Display the map in Streamlit
    st.components.v1.html(m_user._repr_html_(), width=1400, height=800)
