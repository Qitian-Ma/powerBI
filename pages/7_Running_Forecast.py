import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_plotly_events import plotly_events

# Sample data for the bar chart
data = {
    'Category': ['Category A', 'Category B', 'Category C', 'Category D'],
    'Values': [450, 300, 200, 150]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to create an animated bar chart
def create_bar_chart(data, selected_category=None):
    fig = px.bar(data, x='Category', y='Values', title='Interactive Bar Chart with Animation', color_discrete_sequence=px.colors.qualitative.Light24)
    if selected_category:
        fig.update_traces(marker_color=['red' if cat == selected_category else 'dimgrey' for cat in data['Category']])
    return fig

# Initialize Streamlit app
st.title('Interactive Bar Chart Example')

# Use session state to store the selected category
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

# Create the bar chart
chart = create_bar_chart(df, st.session_state.selected_category)

# Display the bar chart and capture click events
selected_points = plotly_events(chart, click_event=True, hover_event=False)

# Capture click events from the bar chart
if selected_points:
    clicked_category = selected_points[0]['x']
    if clicked_category == st.session_state.selected_category:
        st.session_state.selected_category = None
    else:
        st.session_state.selected_category = clicked_category
    st.experimental_rerun()


# Display the clicked category
if st.session_state.selected_category:
    st.write(f'You clicked on: {st.session_state.selected_category}')
