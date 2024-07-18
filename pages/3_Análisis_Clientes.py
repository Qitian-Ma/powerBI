import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from st_aggrid.shared import GridUpdateMode
from load_data import load_data
from util.filter_data import filter_data
from util.expander import set_expander_country, set_expander_client, set_expander_category, set_expander_brand, set_expander_product, set_expander_salesperon, set_date, adjust_for_february
import numpy as np

load_data()

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



start_date = '2023-01-01'
end_date = '2023-12-31'


st.session_state['start_date'], st.session_state['end_date'] = set_date(start_date, end_date)

st.session_state['start_date_past'] = adjust_for_february(st.session_state['start_date'])
st.session_state['end_date_past'] = adjust_for_february(st.session_state['end_date'])

selected_df, selected_past_df = filter_data(st.session_state['country_filter'], st.session_state['product_filter'], st.session_state['brand_filter'], st.session_state['customer_type_filter'], st.session_state['seller_filter'], st.session_state['category_filter'], st.session_state['start_date_past'], st.session_state['start_date'], st.session_state['end_date'], st.session_state['end_date_past'])

selected_customer_df = selected_df.groupby(["Customer No_", "Customer Name"])["Amount"].sum().reset_index()
selected_customer_past_df = selected_past_df.groupby(["Customer No_", "Customer Name"])["Amount"].sum().reset_index()

selected_years_df = selected_customer_df.merge(selected_customer_past_df, on=["Customer No_", "Customer Name"], suffixes=('', ' Año Ant.')).rename({"Amount": "Ventas", "Amount Año Ant.": "Ventas Año Ant."}, axis=1)
selected_years_df["Var Año-a-Año Ventas"] = selected_years_df["Ventas"] - selected_years_df["Ventas Año Ant."]
selected_years_df["% Var Año-a-Año Ventas"] = selected_years_df["Var Año-a-Año Ventas"] / selected_years_df["Ventas Año Ant."].replace(0, np.nan).abs() * 100

st.write(selected_years_df.head())

# Sample sales data for this year and last year
data = {
    'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
    'This Year': [120, 100, 300, 400, 500],
    'Last Year': [100, 250, 150, 300, 450]
}

sales_df = pd.DataFrame(data)

# Function to calculate year-to-year percentage difference and render progress bar
def render_progress_bar(row):
    # this_year = row['This Year']
    # last_year = row['Last Year']
    # if last_year != 0:
    #     percentage_diff = ((this_year - last_year) / abs(last_year)) * 100
    # else:
    #     percentage_diff = 0  # Avoid division by zero
    if row["% Var Año-a-Año Ventas"] == np.nan:
        percentage_diff = 0
    else:
        percentage_diff = row["% Var Año-a-Año Ventas"]
    color = "green" if percentage_diff >= 0 else "red"
    percentage = abs(percentage_diff)
    direction = "left" if percentage_diff >= 0 else "right"
    text_position = "right" if percentage_diff >= 0 else "left"
    color = "green" if percentage_diff >= 0 else "red"
    if percentage_diff >= 0:
        return (
            f'<div style="width: 100px; background-color: #e0e0e0; border-radius: 5px; position: absolute; height: 20px; top: 25%">'
            f'<div style="width: {percentage_diff / 2}%; background-color: {color}; height: 100%; border-radius: 5px; position: absolute; top: 0; left: 50%; transform: translateX(0%);">'
            f'</div>'
            f'</div>'
        ).replace('\n', '')
    else:
        return (
            f'<div style="width: 100px; background-color: #e0e0e0; border-radius: 5px; position: absolute; height: 20px; top: 25%">'
            f'<div style="width: {-percentage_diff / 2}%; background-color: {color}; height: 100%; border-radius: 5px; position: absolute; top: 0; right: 50%; transform: translateX(0%);">'
            f'</div>'
            f'</div>'
        ).replace('\n', '')

# Add a progress column to the sales DataFrame
selected_years_df['Progress'] = selected_years_df.apply(render_progress_bar, axis=1)

# Function to create an interactive table with AgGrid

@st.experimental_fragment
def select_table():
    def aggrid_interactive_table(df: pd.DataFrame):
        options = GridOptionsBuilder.from_dataframe(
            df, enableRowGroup=True, enableValue=True, enablePivot=True, resizable=True, filterable=True, groupable=True, selection_mode='multiple'
        )

        options.configure_side_bar()
        options.configure_selection("single")

        # Add custom cell renderer for the progress column
        cell_renderer = JsCode("""
        class HtmlRenderer {
            init(params) {
                this.eGui = document.createElement('div');
                this.eGui.innerHTML = params.value;
            }
            getGui() {
                return this.eGui;
            }
        }
        """)

        options.configure_column("Progress", header_name="Progress", cellRenderer=cell_renderer)
        
        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            theme="material",
            update_mode=GridUpdateMode.MODEL_CHANGED,
            allow_unsafe_jscode=True,
        )

        return selection

    # Render the interactive table
    selection = aggrid_interactive_table(df=selected_years_df.sort_values(by="Ventas", ascending=False))

    # Display selected rows
    if selection:
        st.write("You selected:")
        st.write(selection["selected_rows"])

select_table()