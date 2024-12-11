from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from jbi100_app.data import get_data

# Load the data
df = get_data()

# Initialize the Dash app
app = Dash()

# Get the range of shark lengths for the slider
shark_length_min = df['Shark.length.m'].min()
shark_length_max = df['Shark.length.m'].max()

# Create the layout
app.layout = html.Div(
    style={"height": "100vh", "width": "100vw", "margin": 0, "padding": 0, "display": "flex"},  # Full-screen container
    children=[
        # Sidebar with dropdown and filters
        html.Div(
            style={"width": "20%", "padding": "10px", "boxShadow": "2px 0px 5px rgba(0, 0, 0, 0.1)"},
            children=[
                dcc.Dropdown(
                    id='shark-dropdown',
                    options=[
                        {"label": shark, "value": shark} for shark in df['Shark.common.name'].unique()
                    ],
                    multi=True,
                    placeholder="Select shark type(s)",
                ),
                html.Div(
                    id='filters-container',
                    style={"display": "none"},  # Initially hidden
                    children=[
                        html.Label("Shark Length (meters):"),
                        dcc.RangeSlider(
                            id='shark-length-slider',
                            min=shark_length_min,
                            max=shark_length_max,
                            step=0.1,
                            marks={
                                i: f"{i:.1f}" for i in [round(x, 1) for x in 
                                    list(np.linspace(shark_length_min, shark_length_max, num=10))]
                            },
                            value=[shark_length_min, shark_length_max],
                        ),
                        html.Label("Provoked Status:"),
                        dcc.RadioItems(
                            id='provoked-status',
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "Provoked", "value": "provoked"},
                                {"label": "Unprovoked", "value": "unprovoked"},
                            ],
                            value="all",
                        ),
                        dcc.Checklist(
                            id='include-unknown-length',
                            options=[{"label": "Include unknown lengths", "value": "include"}],
                            value=[]
                        ),
                    ]
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
                            id='activity-bar-chart',
                            style={"flex": "1"}
                        )
                    ]
                ),
            ]
        ),
    ]
)

# Callback to toggle filter visibility
@app.callback(
    Output('filters-container', 'style'),
    Input('shark-dropdown', 'value')
)
def toggle_filters(selected_shark):
    if selected_shark:
        return {"display": "block"}  # Show filters if a shark is selected
    return {"display": "none"}  # Hide filters otherwise

# Callback to update the map and bar chart
@app.callback(
    [Output('shark-map', 'figure'),
     Output('activity-bar-chart', 'figure')],
    [Input('shark-dropdown', 'value'),
     Input('shark-length-slider', 'value'),
     Input('provoked-status', 'value'),
     Input('include-unknown-length', 'value'),
     Input('map-tabs', 'value')]
)
def update_map_and_chart(selected_sharks, shark_length_range, provoked_status, include_unknown_length, selected_tab):
    # Filter the data based on the selected shark type(s)
    filtered_df = df
    if selected_sharks:
        filtered_df = filtered_df[filtered_df['Shark.common.name'].isin(selected_sharks)]

    # Filter by shark length range
    if 'include' in include_unknown_length:
        filtered_df = filtered_df[(filtered_df['Shark.length.m'].isna()) |
                                   ((filtered_df['Shark.length.m'] >= shark_length_range[0]) &
                                    (filtered_df['Shark.length.m'] <= shark_length_range[1]))]
    else:
        filtered_df = filtered_df[(filtered_df['Shark.length.m'] >= shark_length_range[0]) &
                                   (filtered_df['Shark.length.m'] <= shark_length_range[1])]

    # Filter by provoked status
    if provoked_status != "all":
        filtered_df = filtered_df[filtered_df['Provoked/unprovoked'] == provoked_status]

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
    activity_counts = filtered_df['Victim.activity'].value_counts().reset_index()
    activity_counts.columns = ['Victim.activity', 'Count']
    bar_fig = px.bar(
        activity_counts,
        x='Victim.activity',
        y='Count',
        title="Distribution of Victim.activity",
        labels={"Victim.activity": "Activity Type", "Count": "Count"},
    )

    return map_fig, bar_fig

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)