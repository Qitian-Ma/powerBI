import streamlit.components.v1 as components

def plotly_events(fig, click_event=True, hover_event=False, select_event=False, relayout_event=False):
    event = []
    config = {'displayModeBar': False}

    # Create plotly chart
    html_str = f"""
    <div id="plotly-div"></div>
    <script>
    var plotly_div = document.getElementById('plotly-div');
    Plotly.react(plotly_div, {fig.to_json()}, {fig['layout'].to_json()}, {config});

    plotly_div.on('plotly_click', function(data) {{
        var point = data.points[0];
        var event = {{
            x: point.x,
            y: point.y,
            curveNumber: point.curveNumber,
            pointNumber: point.pointNumber,
            label: point.data.labels[point.pointNumber]
        }};
        var json_event = JSON.stringify(event);
        window.parent.postMessage(json_event, "*");
    }});
    </script>
    """

    event_data = components.html(html_str, height=600)

    if event_data:
        event = [event_data]
    
    return event
