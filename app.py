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
                dcc.Dropdown(
                    id='var-select',
                    options=[
                        {"label": varname, "value": varname} for varname in df.columns.values
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
                            id='activity-bar-chart',
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
     Output('activity-bar-chart', 'figure')],
    [Input('shark-dropdown', 'value'),
     Input('map-tabs', 'value'),
     Input('var-select', 'value')]
)
def update_map_and_chart(selected_shark, selected_tab, selected_var):
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
    activity_counts = filtered_df[selected_var].value_counts().reset_index()
    activity_counts.columns = [selected_var, 'Count']
    bar_fig = px.bar(
        activity_counts,
        x=selected_var,
        y='Count',
        title="Distribution of"+selected_var,
        labels={selected_var: "activity Type", "Count": "Count"},
    )

    return map_fig, bar_fig

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
