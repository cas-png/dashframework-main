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
    style={"height": "100vh", "width": "100vw", "margin": 0, "padding": 0, "display": "flex"},  # Full-screen container
    children=[
        # Sidebar with dropdown
        html.Div(
            style={"width": "20%", "padding": "10px", "boxShadow": "2px 0px 5px rgba(0, 0, 0, 0.1)"},
            children=[
                dcc.Dropdown(
                    id='shark-dropdown',
                    options=[
                        {"label": shark, "value": shark} for shark in df['Shark.common.name'].unique()
                    ],
                    placeholder="Select a shark type",
                ),
            ],
        ),
        # Main content with map and bar chart
        html.Div(
            style={"width": "80%", "display": "flex", "flexDirection": "column", "padding": "10px"},
            children=[
                # Tabs for switching between heatmap and scatter plot
                dcc.Tabs(
                    id="map-tabs",
                    value="heatmap",  # Default tab
                    children=[
                        dcc.Tab(label="Heatmap", value="heatmap"),
                        dcc.Tab(label="Scatter Plot", value="scatter"),
                    ],
                ),
                html.Div(
                    style={"display": "flex", "flexDirection": "row", "height": "100%"},
                    children=[
                        # Map
                        dcc.Graph(
                            id='shark-map',
                            style={"flex": "3", "marginRight": "10px"}
                        ),
                        # Bar chart
                        dcc.Graph(
                            id='injury-bar-chart',
                            style={"flex": "1"}
                        )
                    ]
                ),
            ]
        ),
    ]
)

# Callback to update the map and bar chart
@app.callback(
    [Output('shark-map', 'figure'),
     Output('injury-bar-chart', 'figure')],
    [Input('shark-dropdown', 'value'),
     Input('map-tabs', 'value')]
)
def update_map_and_chart(selected_shark, selected_tab):
    # Filter the data based on the selected shark type
    filtered_df = df
    if selected_shark:
        filtered_df = filtered_df[filtered_df['Shark.common.name'] == selected_shark]

    # Create the map figure
    if selected_tab == "heatmap":
        # Create density map (heatmap)
        map_fig = px.density_mapbox(
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
        map_fig = px.scatter_mapbox(
            filtered_df,
            lat='Latitude',
            lon='Longitude',
            color='Victim.injury',  # Color by incident type
            hover_name='Shark.common.name',  # Display shark name on hover
            center=dict(lat=-23, lon=132),  # Center of Australia
            zoom=3,
            mapbox_style="open-street-map"
        )

    # Create the bar chart figure
    injury_counts = filtered_df['Victim.injury'].value_counts().reset_index()
    injury_counts.columns = ['Victim.injury', 'Count']
    bar_fig = px.bar(
        injury_counts,
        x='Victim.injury',
        y='Count',
        title="Distribution of Victim Injuries",
        labels={"Victim.injury": "Injury Type", "Count": "Count"},
    )

    return map_fig, bar_fig

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
