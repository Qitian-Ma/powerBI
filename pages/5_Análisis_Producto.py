import streamlit as st
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'util'))

from streamlit_plotly_events import plotly_events

flag = False
# Sample data for the pie chart
data = {
    'Category': ['Category A', 'Category B', 'Category C', 'Category D'],
    'Values': [450, 300, 200, 150]
}

# Convert to DataFrame
df = pd.DataFrame(data)

cat_dict = {0:'Category A', 1:'Category B', 2:'Category C', 3:'Category D'}

# Function to create a pie chart
def create_pie_chart(data, selected_category=None):
    fig = px.pie(data, names='Category', values='Values', title='Interactive Pie Chart', color_discrete_sequence=px.colors.qualitative.Plotly)
    if selected_category:
        fig.update_traces(pull=[0.1 if cat == selected_category else 0 for cat in data['Category']])
    return fig

# Initialize Streamlit app
st.title('Interactive Pie Chart Example')

# Use session state to store the selected category
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None


# Create the pie chart
chart = create_pie_chart(df, st.session_state.selected_category)


# Display the pie chart and capture click events
selected_points = plotly_events(chart, click_event=True, hover_event=False)
    

# Capture click events from the pie chart


# Display the updated pie chart with the selected category highlighted

# st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})


if selected_points:
    selected_category = cat_dict[selected_points[0]["pointNumber"]]
    st.session_state.selected_category = selected_category
    # chart = create_pie_chart(df, cat_dict[st.session_state.selected_category["pointNumber"]])
    # st.plotly_chart(chart, use_container_width=True)
    st.experimental_rerun()
# Display the clicked category
if st.session_state.selected_category:
    st.write(f'You clicked on: {st.session_state.selected_category}')
