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
        # Graph displaying the density map
        dcc.Graph(
            id='shark-map',
            style={"height": "90%", "width": "100%"}  # Full-screen graph
        )
    ]
)

# Callback to update the map based on dropdown selection
@app.callback(
    Output('shark-map', 'figure'),
    [Input('shark-dropdown', 'value')]
)
def update_map(selected_shark):
    if selected_shark:
        filtered_df = df[df['Shark.common.name'] == selected_shark]
    else:
        filtered_df = df  # Show all data if no shark is selected

    # Create density map figure
    fig = px.density_mapbox(
        filtered_df,
        lat='Latitude',
        lon='Longitude',
        radius=5,
        center=dict(lat=-23, lon=132),#center of australia
        zoom=3,
        mapbox_style="open-street-map"
    )
    return fig

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
