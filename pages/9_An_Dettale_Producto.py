import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from streamlit_plotly_events import plotly_events

# Sample data for the pie chart
data = {
    'Category': ['Category A', 'Category B', 'Category C', 'Category D'],
    'Values': [450, 300, 200, 150]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to create a pie chart using plotly.graph_objects
def create_pie_chart(selected_category=None):
    fig = go.Figure(
        data=[go.Pie(
            labels=df['Category'],
            values=df['Values'],
            hole=.3,
            pull=[0.1 if cat == selected_category else 0 for cat in df['Category']]
        )]
    )
    fig.update_layout(title_text='Interactive Pie Chart')
    return fig

# Initialize Streamlit app
st.title('Interactive Pie Chart Example')

# Use session state to store the selected category
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

# Create the pie chart
chart = create_pie_chart(st.session_state.selected_category)

selected_points = plotly_events(chart, click_event=True, hover_event=False)
# fig = st.plotly_chart(chart, use_container_width=True)
# if selected_points:
#     clicked_category = selected_points[0]
#     st.session_state.selected_category = clicked_category

# Display the pie chart
# fig = st.plotly_chart(chart, use_container_width=True)

# Update the pie chart with the selected category highlighted
chart = create_pie_chart(st.session_state.selected_category)
# fig = st.plotly_chart(chart, use_container_width=True)

# Display the clicked category
if st.session_state.selected_category:
    st.write(f'You clicked on: {st.session_state.selected_category}')
