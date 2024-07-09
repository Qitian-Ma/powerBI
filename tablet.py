


# Custom CSS for styling
custom_css = """
<style>
.sales-widget {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    color: #333333;
    width: 300px;
    margin: 20px auto;
    text-align: center;
    font-family: 'Arial', sans-serif;
}

.sales-widget h2 {
    margin-bottom: 10px;
    font-size: 24px;
    color: #5A9BD5;
}

.sales-widget .value {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
}

.sales-widget .previous {
    font-size: 20px;
    color: #777777;
    margin-bottom: 10px;
}

.sales-widget .difference {
    font-size: 24px;
    margin-top: 10px;
    padding: 10px;
    border-radius: 5px;
}

.sales-widget .difference.negative {
    color: #ff4d4f;
    background-color: #ffe6e6;
}

.sales-widget .difference.positive {
    color: #52c41a;
    background-color: #e6ffe6;
}
</style>
"""


# HTML for the sales widget


def get_html(name, current_sales, previous_sales, diff_percentage):
    return  f"""
<div class="sales-widget">
    <h2>{name}</h2>
    <div class="value">€ {current_sales:,.0f}</div>
    <div class="previous">Año Ant.: € {previous_sales:,.0f}</div>
    <div class="difference {'negative' if diff_percentage < 0 else 'positive'}">{diff_percentage:.1f} %</div>
</div>
"""