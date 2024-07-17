import streamlit as st
from .expander import adjust_for_february

@st.experimental_fragment
def plot_lineChart(selected_df, selected_past_df):

    def resample_df(freq):
        selected_date_df = selected_df[['Posting Date', 'Amount']].set_index('Posting Date').resample(freq).sum().sort_values(by=['Posting Date']).reset_index()
        selected_date_past_df = selected_past_df[['Posting Date', 'Amount']].set_index('Posting Date').resample(freq).sum().sort_values(by=['Posting Date']).reset_index()
        selected_date_past_df['Posting Date'] = selected_date_past_df['Posting Date'].apply(lambda date: adjust_for_february(date, -1))
        selected_date_all_df = selected_date_df.merge(selected_date_past_df, how='outer', on='Posting Date', suffixes=["_now", "_past"]).reset_index()

        return selected_date_all_df

    aggregation = st.selectbox("Select aggregation level", ["Day", "Month", "Quarter"])

    # Aggregate data based on user selection
    if aggregation == "Day":
        freq = 'D'
        st.subheader("Daily Sales Data")
    elif aggregation == "Month":
        freq = 'M'
        st.subheader("Monthly Sales Data")
    elif aggregation == "Quarter":
        freq = 'Q'
        st.subheader("Quarterly Sales Data")

    selected_date_all_df = resample_df(freq)

    st.line_chart(
        data=selected_date_all_df,
        x='Posting Date',
        y=['Amount_past', 'Amount_now'],
        y_label = 'Sales',
        x_label = 'Date',
        color=["#619CFF", "#F8766D"])