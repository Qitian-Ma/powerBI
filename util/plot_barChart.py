import streamlit as st

@st.experimental_fragment
def plot_barChart(selected_customer_all_df):
    import numpy as np
    import plotly.graph_objects as go

    top_k = st.selectbox("Top k Clients", [25, 50, 100])

    selected_customer_all_df = selected_customer_all_df.sort_values(by='Ventas', ascending=True).dropna().tail(top_k)

    selected_customer_all_df["Var Año-a-Año Ventas"] = selected_customer_all_df["Ventas"] - selected_customer_all_df["Ventas Año Ant."]
    selected_customer_all_df["% Var Año-a-Año Ventas"] = (selected_customer_all_df["Var Año-a-Año Ventas"] / selected_customer_all_df["Ventas Año Ant."].replace(0, np.nan) * 100).round(2)

    selected_customer_all_df['Var pos Año-a-Año Ventas'] = selected_customer_all_df["Var Año-a-Año Ventas"].apply(lambda x: max(x, 0))
    selected_customer_all_df['Var neg Año-a-Año Ventas'] = selected_customer_all_df["Var Año-a-Año Ventas"].apply(lambda x: min(x, 0))
    selected_customer_all_df = selected_customer_all_df.reset_index().drop(['index'], axis=1)

# Streamlit Application
    st.title('Comparative Sales Analysis')

    # Table display toggle
    if st.checkbox("Show Data Table"):
        st.dataframe(selected_customer_all_df)

    # Filters for interactivity

    # Filter data based on selection
    filtered_df = selected_customer_all_df

    # Interactive Plotly Bar Chart
    fig = go.Figure()

    max_sale = max(filtered_df['Ventas Año Ant.'].max(), filtered_df["Ventas"].max())


    fig.add_trace(go.Bar(
        y=filtered_df['Customer Name'],
        x=filtered_df['Ventas Año Ant.'],
        name='Ventas Año Ant.',
        orientation='h',
        marker=dict(color='lightgrey')
    ))

    fig.add_trace(go.Bar(
        y=filtered_df['Customer Name'],
        x=filtered_df['Var pos Año-a-Año Ventas'],
        name='Var pos Año-a-Año Ventas',
        orientation='h',
        marker=dict(color='rgb(255,72,105)')
    ))

    fig.add_trace(go.Bar(
        y=filtered_df['Customer Name'],
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
            x=max(row['Ventas'], 0)  + max_sale / 10 if row['Var pos Año-a-Año Ventas'] > 0 else max(row['Ventas Año Ant.'], 0) + max_sale / 10,
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
        height=top_k * 30,
        width=1500
    )

    st.plotly_chart(fig)