from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
from dash import html, dcc, Dash
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

from jbi100_app.data import get_data

df = get_data()

# Create density map figure
fig = px.density_mapbox(
    df,
    lat='Latitude',
    lon='Longitude',
    radius=5,
    center=dict(lat=0, lon=180),
    zoom=3,
    mapbox_style="open-street-map"
)

# Initialize the Dash app
app = Dash()

# Define the layout
app.layout = html.Div(
    style={"height": "100vh", "width": "100vw", "margin": 0, "padding": 0},  # Full-screen container
    children=[
        dcc.Graph(
            figure=fig,
            style={"height": "100%", "width": "100%"}  # Full-screen graph
        )
    ]
)

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)