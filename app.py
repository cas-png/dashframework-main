from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
from jbi100_app.data import get_data

# Load the data
df = get_data()

# Ensure that there's a 'Year' column in df. If not, you might need to extract the year from a date field.
# For example, if there's a 'Date' column with datetime objects, you can do:
# df['Year'] = df['Date'].dt.year

# Initialize the Dash app
app = Dash()

# Get the range of shark lengths for the slider
shark_length_min = df['Shark.length.m'].min()
shark_length_max = df['Shark.length.m'].max()

# Get the range of years for the year slider
year_min = df['Incident.year'].min()
year_max = df['Incident.year'].max()

# Create the layout
app.layout = html.Div(style={"height": "98vh", "width": "98vw", "margin": 0, "padding": 0, "display": "flex"}, children=[ # Full-screen container
    # Sidebar with dropdown and filters --- TODO: Add more filters
    html.Div(style={'width': '20%', 'padding': '10px', 'float': 'left', "border": "1px solid rgba(0, 0, 0, 1)", "border-radius": "10px", "boxShadow": "5px 5px 5px rgba(0, 0, 0, 0.3)"}, children=[
        # html.H1("Shark Attack Data"),
        # Dropdown for selecting shark type
        html.Label("Shark Type:"),
        dcc.Dropdown(
            id='shark-dropdown',
            options=[{"label": shark, "value": shark} for shark in df['Shark.full.name'].unique()],
            multi=True,
            placeholder="Select shark type(s)",
        ),
                html.Br(),
        # Dropdown for selecting injury level
        html.Label("Victim Injury Level:"),
        dcc.Dropdown(
            id='injury-dropdown',
            options=[{"label": level, "value": level} for level in df['Victim.injury'].unique()],
            multi=True,
            placeholder="Select injury level(s)",
        ),
        html.Br(),
        # Range slider for shark length
        html.Label("Shark Length (meters):"),
        dcc.RangeSlider(
            id='shark-length-slider',
            min=shark_length_min,
            max=shark_length_max,
            step=0.1,
            marks={i: f"{i:.1f}" for i in np.linspace(shark_length_min, shark_length_max, num=10)},
            value=[shark_length_min, shark_length_max],
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.Br(),
        # Checkbox for including unknown lengths
        dcc.Checklist(
            id='include-unknown-length',
            options=[{"label": "Include unknown lengths", "value": "include"}],
            value=[]
        ),
        html.Br(),
        # Radio items for provoked status
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
        html.Br(),
        # Reset filters button
        html.Button(
            "Reset Filters",
            id='reset-filters-button',
            style={"marginTop": "10px"}
        ),
        html.Br(),
        # Display the percentage of rows kept after filtering
        html.Div(style={"marginTop": "10px", "display": "flex", "flexDirection": "row"}, children=[
            html.Label("After filtering, ", style={'white-space': 'pre'}),
            html.Div(id='row-number'),
            html.Label(" rows are kept", style={'white-space': 'pre'}),
        ]),
        html.Div(style={"display": "flex", "flexDirection": "row"}, children=[
            html.Label("("),
            html.Div(id='row-percentage'),
            html.Label("% of total rows).")
        ]),
    ]),
    
    # Main content with map and timeline --- TODO: Add a timeline
    html.Div(style={"width": "60%", "display": "flex", "flexDirection": "column", "padding": "10px"}, children=[
        # Tabs for switching between heatmap and scatter plot
        dcc.Tabs(
            id="map-tabs",
            value="heatmap",  # Default tab
            children=[
                dcc.Tab(label="Heatmap", value="heatmap"),
                dcc.Tab(label="Scatter Plot", value="scatter"),
            ],
        ),
        html.Div(style={"display": "flex", "flexDirection": "column", "height": "100%", "padding": "10px"}, children=[
            dcc.Graph(id='shark-map', style={"flex": "3", "marginRight": "10px"}),
            # Year Range Slider below the map
            html.Label(id='slider-label'),  # Create a label for dynamic updates
            dcc.RangeSlider(
                id='year-slider',
                min=year_min,
                max=year_max,
                step=1,
                marks={year: str(year) for year in range(year_min, year_max+1, 10)},
                value=[year_min, year_max],
                tooltip={"placement": "bottom", "always_visible": True}  # Enable tooltip
            ),
        ]),
    ]),
    
    # Bar chart for distributions --- TODO: Allow for changing the bar chart to show different data
    html.Div(style={'width': '20%', 'padding': '10px', "border": "1px solid rgba(0, 0, 0, 1)", "border-radius": "10px", "boxShadow": "-5px 5px 5px rgba(0, 0, 0, 0.3)", "display": "flex", "flexDirection": "column"}, children=[
        dcc.Graph(id='activity-bar-chart', style={"flex": "1"}),
    ]),
])

# Callback to update the map and bar chart
@app.callback(
    [
        Output('shark-map', 'figure'),
        Output('activity-bar-chart', 'figure'),
        Output('row-percentage', 'children'),
        Output('row-number', 'children'),
    ],
    [
        Input('shark-dropdown', 'value'),
        Input('injury-dropdown', 'value'),
        Input('shark-length-slider', 'value'),
        Input('provoked-status', 'value'),
        Input('include-unknown-length', 'value'),
        Input('map-tabs', 'value'),
        Input('year-slider', 'value')
    ]
)
def update_map_and_chart(selected_sharks, selected_injuries, shark_length_range, provoked_status, include_unknown_length, selected_tab, year_range):

    filtered_df = df

        # Filter the data based on the selected shark type(s)
    if selected_sharks:
        filtered_df = filtered_df[filtered_df['Shark.full.name'].isin(selected_sharks)]
    # Filter the data based on the selected injury level(s)
    if selected_injuries:
        filtered_df = filtered_df[filtered_df['Victim.injury'].isin(selected_injuries)]

    # Filter by shark length range
    if 'include' in include_unknown_length:
        filtered_df = filtered_df[
            (filtered_df['Shark.length.m'].isna()) |
            ((filtered_df['Shark.length.m'] >= shark_length_range[0]) & (filtered_df['Shark.length.m'] <= shark_length_range[1]))
        ]
    else:
        filtered_df = filtered_df[
            (filtered_df['Shark.length.m'] >= shark_length_range[0]) &
            (filtered_df['Shark.length.m'] <= shark_length_range[1])
        ]

    # Filter by provoked status
    if provoked_status != "all":
        filtered_df = filtered_df[filtered_df['Provoked/unprovoked'] == provoked_status]

    # Filter by year range
    filtered_df = filtered_df[
        (filtered_df['Incident.year'] >= year_range[0]) &
        (filtered_df['Incident.year'] <= year_range[1])
    ]

    # Calculate the percentage of rows that were kept after filtering
    row_percentage =  np.round(len(filtered_df)/len(df)*100,2)
    row_number = len(filtered_df)
    
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
    else:  # selected_tab == "scatter"
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

    return map_fig, bar_fig, row_percentage, row_number

# Callback to reset filters
@app.callback(
    [
        Output('shark-dropdown', 'value'),
        Output('shark-length-slider', 'value'),
        Output('provoked-status', 'value'),
        Output('include-unknown-length', 'value'),
        Output('year-slider', 'value')
    ],
    Input('reset-filters-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    # Reset all filter components to their defaults
    return (
        None, 
        [shark_length_min, shark_length_max], 
        "all", 
        [],
        [year_min, year_max]
    )

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
