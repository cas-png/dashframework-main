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
<<<<<<< Updated upstream
app.layout = html.Div(
    style={"height": "100vh", "width": "100vw", "margin": 0, "padding": 0, "display": "flex"},  # Full-screen container
    children=[
        # Sidebar with dropdown
        html.Div(
            style={"width": "20%", "padding": "10px", "boxShadow": "2px 0px 5px rgba(0, 0, 0, 0.1)"},
=======
app.layout = html.Div(style={"height": "98vh", "width": "98vw", "margin": 0, "padding": 0, "display": "flex"}, children=[ # Full-screen container
    # Sidebar with dropdown and filters --- TODO: Add more filters and finish the modal for extra info (link to data source, and descriptions of each variable shown, make sure all variables used in the tool are included)
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
        html.Div(id='row-details', style={"marginTop": "10px"}),
        # Modal for extra info
        dbc.Button("Open modal", id="open-dismiss"),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Dismissing"), close_button=False
                ),
                dbc.ModalBody(children=[
                    dash_table.DataTable([{"Variable Name": value, "Column Name": key} for key, value in categories.items()]),
                    html.Textarea("Shark.full.name is based on Shark.common.name and Shark.scientific.name.", style={"width": "100%", "height": "100px"})
            ]),
                dbc.ModalFooter(dbc.Button("Close", id="close-dismiss")),
            ],
            id="modal-dismiss",
            # keyboard=False,
            # backdrop="static",
        ),
    ]),
    
    html.Div(
    style={"width": "100%", "display": "flex", "flexDirection": "column"},
    children=[
        # Tabs for switching between heatmap and scatter plot
        dcc.Tabs(
            id="map-tabs",
            value="heatmap",  # Default tab
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
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
=======

        # ### CHANGED: Make this Div the parent container for both graphs,
        # with enough height to hold them
        html.Div(
            style={
                "display": "flex",
                "flexDirection": "column",
                "height": "80%",   # adjust as needed
                "padding": "0px"
            },
            children=[
                # ### CHANGED: Make the map figure occupy 80% of the container
                html.Div(
                    style={"display": "flex", "height": "80%", "width": "100%"},
                    children=[
                        dcc.Graph(
                            id='shark-map',
                            style={"width": "100%", "height": "100%"}  # fill parent Div
                        )
                    ]
                ),
                # ### CHANGED: Make the timeline figure occupy 20% of the container
                html.Div(
                    style={"display": "flex", "height": "20%", "width": "100%"},
                    children=[
                        dcc.Graph(
                            id='timeline',
                            style={"width": "100%", "height": "100%"}  # fill parent Div
                        )
                    ]
                ),
            ],
        ),

        # Keep the year range slider and label OUTSIDE the 80/20 container
        html.Label(id='slider-label'),  # Create a label for dynamic updates
        dcc.RangeSlider(
            id='year-slider',
            min=year_min,
            max=year_max,
            step=1,
            marks={year: str(year) for year in range(year_min, year_max + 1, 10)},
            value=[year_min, year_max],
            tooltip={"placement": "bottom", "always_visible": False},  # Enable tooltip
            allowCross=False,
            dots=False
        ),
    ],
),

    
    # Bar chart for distributions
    html.Div(style={'width': '20%', 'padding': '10px', "border": "1px solid rgba(0, 0, 0, 1)", "border-radius": "10px", "boxShadow": "-5px 5px 5px rgba(0, 0, 0, 0.3)", "display": "flex", "flexDirection": "column"}, children=[
        dcc.Dropdown(
            id='var-select',
            options=[
                {"label": categories[category], "value": category} for category in categories
                # {"label": varname, "value": varname} for varname in df.columns.values
                # {"label": "Incident Month", "value": "Incident.month"},
                # {"label": "Victim Injury Severity", "value": "Injury.severity"},
                # {"label": "Victim Injury Result", "value": "Victim.injury"},
                # {"label": "State", "value": "State"},
                # {"label": "Location Type", "value": "Site.category"},
                # {"label": "Shark Type", "value": "Shark.full.name"},
                # {"label": "Provoked", "value": "Provoked/unprovoked"},
                # {"label": "Victim Activity", "value": "Victim.activity"},
                # {"label": "Victim Gender", "value": "Victim.gender"},
                # {"label": "Source Type", "value": "Data.source"},
            ],
            placeholder="Select a variable",
            value="Victim.injury"
>>>>>>> Stashed changes
        ),
    ]
)

# Callback to update the map and bar chart
@app.callback(
    [Output('shark-map', 'figure'),
     Output('activity-bar-chart', 'figure')],
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
    activity_counts = filtered_df['Victim.activity'].value_counts().reset_index()
    activity_counts.columns = ['Victim.activity', 'Count']
    bar_fig = px.bar(
        activity_counts,
        x='Victim.activity',
        y='Count',
        title="Distribution of Victim.activity",
        labels={"Victim.activity": "activity Type", "Count": "Count"},
    )

    return map_fig, bar_fig

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
