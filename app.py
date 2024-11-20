from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from jbi100_app.data import get_data

# Load the data
df = get_data()

# Initialize the Dash app
app = Dash()

# Create the layout
app.layout = html.Div(
    style={"height": "100vh", "width": "100vw", "margin": 0, "padding": 0},  # Full-screen container
    children=[
        # Dropdown menu for filtering by shark type
        html.Div(
            style={"width": "300px", "padding": "10px"},
            children=[
                dcc.Dropdown(
                    id='shark-dropdown',
                    options=[
                        {"label": shark, "value": shark} for shark in df['Shark.common.name'].unique()
                    ],
                    placeholder="Select a shark type",
                )
            ],
        ),
        # Tabs for switching between heatmap and scatter plot
        dcc.Tabs(
            id="map-tabs",
            value="heatmap",  # Default tab
            children=[
                dcc.Tab(label="Heatmap", value="heatmap"),
                dcc.Tab(label="Scatter Plot", value="scatter"),
            ],
        ),
        # Graph displaying the map
        dcc.Graph(
            id='shark-map',
            style={"height": "85%", "width": "100%"}  # Full-screen graph
        )
    ]
)

# Callback to update the map based on dropdown selection and selected tab
@app.callback(
    Output('shark-map', 'figure'),
    [Input('shark-dropdown', 'value'),
     Input('map-tabs', 'value')]
)
def update_map(selected_shark, selected_tab):
    if selected_shark:
        filtered_df = df[df['Shark.common.name'] == selected_shark]
    else:
        filtered_df = df  # Show all data if no shark is selected

    if selected_tab == "heatmap":
        # Create density map (heatmap)
        fig = px.density_mapbox(
            filtered_df,
            lat='Latitude',
            lon='Longitude',
            radius=5,
            center=dict(lat=-23, lon=132),  # Center of Australia
            zoom=3,
            mapbox_style="open-street-map"
        )
    elif selected_tab == "scatter":
        # Create scatter plot map
        fig = px.scatter_mapbox(
            filtered_df,
            lat='Latitude',
            lon='Longitude',
            color='Victim.injury',  # Color by incident type
            hover_name='Shark.common.name',  # Display shark name on hover
            center=dict(lat=-23, lon=132),  # Center of Australia
            zoom=3,
            mapbox_style="open-street-map"
        )
    return fig

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
