from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from pandas import wide_to_long

from jbi100_app.data import get_data
import plotly.graph_objects as go

# Load the data
df = get_data()

# Ensure that there's a 'Year' column in df. If not, you might need to extract the year from a date field.
# For example, if there's a 'Date' column with datetime objects, you can do:
# df['Year'] = df['Date'].dt.year

# Initialize the Dash app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Get the range of shark lengths for the slider
shark_length_min = df['Shark.length.m'].min()
shark_length_max = df['Shark.length.m'].max()

# Get the range of years for the year slider
year_min = df['Incident.year'].min()
year_max = df['Incident.year'].max()

categories = {"Incident.month": "Incident Month", 
              "Injury.severity": "Victim Injury Severity", 
              "Victim.injury": "Victim Injury Result", 
              "State": "State", 
              "Site.category": "Location Type", 
              "Shark.common.name": "Shark Type",
              "Provoked/unprovoked": "Provoked", 
              "Victim.activity": "Victim Activity",
              "Victim.gender": "Victim Gender",
              "Data.source": "Source Type"}

category_info = {"Incident Date": "Based on Incident.year and Incident.month", 
                 "Victim Injury Severity": "Injury.severity", 
                 "Victim Injury Result": "Victim.injury", 
                 "State": "State", 
                 "Location Type": "Site.category", 
                 "Shark Type": "Shark.common.name",
                 "Provoked": "Provoked/unprovoked", 
                 "Victim Activity": "Victim.activity",
                 "Victim Gender": "Victim.gender",
                 "Source Type": "Data.source",
                 "Shark Length": "Shark.length.m"} #TODO double check if this is correct and complete

# Create the layout
app.layout = html.Div(style={"height": "98vh", "width": "98vw", "margin": 0, "padding": 0, "display": "flex"}, children=[ # Full-screen container
    # Sidebar with dropdown and filters --- TODO: Add more filters and finish the modal for extra info (link to data source, and descriptions of each variable shown, make sure all variables used in the tool are included)
    html.Div(style={'width': '15%', 'padding': '10px', 'float': 'left', "border": "1px solid rgba(0, 0, 0, 1)", "border-radius": "10px", "boxShadow": "5px 5px 5px rgba(0, 0, 0, 0.3)", "fontSize": "12px"}, children=[
        # html.H1("Shark Attack Data"),
        # Dropdown for selecting shark type
        html.Label("Shark Type:"),
        dcc.Dropdown(
            id='shark-dropdown',
            options=[{"label": shark, "value": shark} for shark in df['Shark.common.name'].unique()],
            multi=True,
            placeholder="Select shark type(s)",
            style={"fontSize": "12px", "maxHeight": "100px"}
        ),
        # Dropdown for selecting injury level
        html.Label("Victim Injury Level:"),
        dcc.Dropdown(
            id='injury-dropdown',
            options=[{"label": level, "value": level} for level in df['Victim.injury'].unique()],
            multi=True,
            placeholder="Select injury level(s)",
        ),
        # Dropdown for selecting injury severity
        html.Label("Victim Injury Severity:"),
        dcc.Dropdown(
            id='injury-severity-dropdown',
            options=[{"label": level, "value": level} for level in df['Injury.severity'].unique()],
            multi=True,
            placeholder="Select injury severity(s)",
        ),
        # Dropdown for selecting injury severity
        html.Label("State:"),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{"label": level, "value": level} for level in df['State'].unique()],
            multi=True,
            placeholder="Select state(s)",
        ),
        #Site.category
        html.Label("Location Type:"),
        dcc.Dropdown(
            id='site-dropdown',
            options=[{"label": level, "value": level} for level in df['Site.category'].unique()],
            multi=True,
            placeholder="Select state(s)",
        ),
        #Victim.gender
        html.Label("Victim Gender:"),
        dcc.Dropdown(
            id='gender-dropdown',
            options=[{"label": level, "value": level} for level in df['Victim.gender'].unique()],
            multi=True,
            placeholder="Select gender(s)",
        ),
        #Data.source
        html.Label("Data Source:"),
        dcc.Dropdown(
            id='source-dropdown',
            options=[{"label": level, "value": level} for level in df['Data.source'].unique()],
            multi=True,
            placeholder="Select source(s)",
        ),
        #Victim.activity
        html.Label("Victim Activity:"),
        dcc.Dropdown(
            id='victim-activity-dropdown',
            options=[{"label": level, "value": level} for level in df['Victim.activity'].unique()],
            multi=True,
            placeholder="Select activity(s)",
        ),
        # Dropdown for provoked status
        html.Label("Provoked Status:"),
        dcc.Dropdown(
            id='provoked-status',
            options=[{"label": level, "value": level} for level in df['Provoked/unprovoked'].unique()],
            multi=True,
            placeholder="Select provoked status",
        ),
        # html.Br(),
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
        # html.Br(),
        # Checkbox for including unknown lengths
        dcc.Checklist(
            id='include-unknown-length',
            options=[{"label": " Include unknown lengths", "value": "include"}],
            value=["include"]
        ),
        # html.Br(),
        # Reset filters button
        html.Button(
            "Reset Filters",
            id='reset-filters-button',
        ),
        html.Br(),
        html.Div(id='row-details'),
        # Modal for extra info
        dbc.Button("Info", id="open-dismiss"),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle("Tool and Data Information"), close_button=False
                ),
                dbc.ModalBody(children=[
                    html.Div("The table below lists each variable shown in the tool and provides the columns from the data source that are used in that variable."),
                    dash_table.DataTable([{"Variable Name": key, "Details": value} for key, value in category_info.items()]),
                    html.Div("Tool created by JBI100 team 30 (2024 Q2)."),
                    dbc.Button("Visualisation Tool GitHub", href="https://github.com/cas-png/dashframework-main"),
                    dbc.Button("Data Source GitHub", href="https://github.com/cjabradshaw/AustralianSharkIncidentDatabase"),
                    dbc.Button("Video Presentation", href="/"),
            ]),
                dbc.ModalFooter(dbc.Button("Close", id="close-dismiss"), className="justify-content-center")
            ],
            id="modal-dismiss",
            # keyboard=False,
            # backdrop="static",
            fullscreen=True,
        ),
    ]),
    
    # Main content with map and timeline ---
    html.Div(style={"width": "45%", "display": "flex", "flexDirection": "column"}, children=[
        # Tabs for switching between heatmap and scatter plot
        dcc.Tabs(
            id="map-tabs",
            value="scatter",  # Default tab
            children=[
                dcc.Tab(label="Scatter Plot", value="scatter"),
                dcc.Tab(label="Heatmap", value="heatmap"),
            ],
        ),
        html.Div(style={"display": "flex", "flexDirection": "column", "height": "100%"}, children=[
            html.Div(style={"display": "flex", "height": "65%", "width": "100%"}, children=[dcc.Graph(id='shark-map', style={"width": "100%", "height": "100%", "border": "2px solid black"}, config={"scrollZoom": True})]),
            html.Div(style={"display": "flex", "height": "25%", "width": "100%"}, children=[dcc.Graph(id='timeline', style={"width": "100%", "height": "100%", "border": "2px solid red"})]),
            
            # Year Range Slider below the map
            html.Label(id='slider-label'),  # Create a label for dynamic updates
            dcc.RangeSlider(
                id='year-slider',
                min=year_min,
                max=year_max,
                step=1,
                marks={year: str(year) for year in range(year_min, year_max+1, 10)},
                value=[year_min, year_max],
                tooltip={"placement": "bottom", "always_visible": False}, # Enable tooltip
                allowCross=False,
                dots=False
            ),
        ]),
    ]),
    
    # Bar chart for distributions
    html.Div(style={'width': '40%', 'padding': '10px', "border": "1px solid rgba(0, 0, 0, 1)", "border-radius": "10px", "boxShadow": "-5px 5px 5px rgba(0, 0, 0, 0.3)", "display": "flex", "flexDirection": "column"}, children=[
        dcc.Dropdown(
            id='var-select',
            options=[
                {"label": categories[category], "value": category} for category in categories
            ],
            placeholder="Select a variable",
            value="Victim.injury",
            clearable=False
        ),
        dcc.Dropdown(
            id='var-select2',
            options=[
                {"label": categories[category], "value": category} for category in categories
            ],
            placeholder="Select a variable",
            value="Provoked/unprovoked",
            clearable=False
        ),
        html.Div([
            html.Button("Switch Axes for Bar Chart 1", id='switch-axes-bar1', n_clicks=0),
            html.Button("Switch Axes for Bar Chart 2", id='switch-axes-bar2', n_clicks=0),
            ], style={'display': 'flex', 'justify-content': 'space-between', 'margin': '10px 0'}
        ),
        html.Div(style={"display": "flex", "flexDirection": "row", "flex": "1", "width": "100%", "height": "50%"}, children=[
            dcc.Graph(id='activity-bar-chart', style={"flex": "1", "width": "100%", "height": "100%", "border": "2px solid red"}),
            dcc.Graph(id='activity-bar-chart2', style={"flex": "1", "width": "100%", "height": "100%", "border": "2px solid black"}),
        ]),
        html.Div(style={"display": "flex", "flexDirection": "column", "width": "100%", "height": "35%"}, children=[
        dcc.Graph(id='heat-chart', style={"flex": "1", "width": "100%", "height": "100%", "border": "2px solid blue"})])
    ]),
])

# Callback to update the map and bar chart
@app.callback(
    [
        Output('shark-map', 'figure'),
        Output('activity-bar-chart', 'figure'),
        Output('activity-bar-chart2', 'figure'),
        Output('heat-chart', 'figure'),        
        Output('timeline', 'figure'),
        Output('row-details', 'children')
    ],
    [
        Input('shark-dropdown', 'value'),
        Input('injury-dropdown', 'value'),
        Input('injury-severity-dropdown', 'value'),
        Input('victim-activity-dropdown', 'value'),
        Input('source-dropdown', 'value'),
        Input('gender-dropdown', 'value'),
        Input('site-dropdown', 'value'),
        Input('state-dropdown', 'value'),
        Input('shark-length-slider', 'value'),
        Input('provoked-status', 'value'),
        Input('include-unknown-length', 'value'),
        Input('map-tabs', 'value'),
        Input('year-slider', 'value'),
        Input('var-select', 'value'),
        Input('var-select2', 'value'),
        Input('switch-axes-bar1', 'n_clicks'),
        Input('switch-axes-bar2', 'n_clicks')
    ]
)
def update_map_and_chart(selected_sharks, selected_injuries, selected_injury_severities, selected_activities, selected_sources, selected_genders, selected_sites, selected_states, shark_length_range, provoked_status, include_unknown_length, selected_tab, year_range, selected_var, selected_var2, n_clicks_bar1, n_clicks_bar2):

    filtered_df = df

    # Filter the data based on the selected shark type(s)
    if selected_sharks:
        filtered_df = filtered_df[filtered_df['Shark.common.name'].isin(selected_sharks)]
    # Filter the data based on the selected injury level(s)
    if selected_injuries:
        filtered_df = filtered_df[filtered_df['Victim.injury'].isin(selected_injuries)]
    # Filter the data based on the selected injury severity(s)
    if selected_injury_severities:
        filtered_df = filtered_df[filtered_df['Injury.severity'].isin(selected_injury_severities)]
    # Filter the data based on the selected injury severity(s)
    if selected_activities:
        filtered_df = filtered_df[filtered_df['Victim.activity'].isin(selected_activities)]
    # Filter the data based on the selected data source(s)
    if selected_sources:
        filtered_df = filtered_df[filtered_df['Data.source'].isin(selected_sources)]
    # Filter the data based on the selected gender(s)
    if selected_genders:
        filtered_df = filtered_df[filtered_df['Victim.gender'].isin(selected_genders)]
    # Filter the data based on the selected site(s)
    if selected_sites:
        filtered_df = filtered_df[filtered_df['Site.category'].isin(selected_sites)]
    # Filter the data based on the selected state(s)
    if selected_states:
        filtered_df = filtered_df[filtered_df['State'].isin(selected_states)]
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
    if provoked_status:
        filtered_df = filtered_df[filtered_df['Provoked/unprovoked'].isin(provoked_status)]
    # if provoked_status != "all":
    #     filtered_df = filtered_df[filtered_df['Provoked/unprovoked'] == provoked_status]

    # Filter by year range
    filtered_df = filtered_df[
        (filtered_df['Incident.year'] >= year_range[0]) &
        (filtered_df['Incident.year'] <= year_range[1])
    ]

    # Calculate the percentage of rows that were kept after filtering
    row_percentage =  np.round(len(filtered_df)/len(df)*100,2)
    row_number = len(filtered_df)
    row_details = f"After filtering, {row_number} rows are kept ({row_percentage}% of total rows)."
    if row_number == 1:
        row_details = f"After filtering, {row_number} row is kept ({row_percentage}% of total rows)."
    
    # Create the map figure
    if selected_tab == "heatmap":
        # Create density map (heatmap)
        map_fig = px.density_mapbox(
            filtered_df,
            lat='Latitude',
            lon='Longitude',
            radius=5,
            center=dict(lat=-28, lon=130), #center=dict(lat=-23, lon=132),  # Center of Australia
            zoom=2.5,
            mapbox_style="open-street-map"
        )
    else:  # selected_tab == "scatter"
        # Create scatter plot map
        map_fig = px.scatter_mapbox(
            filtered_df,
            lat='Latitude',
            lon='Longitude',
            color=selected_var,  # Color by incident type
            hover_name='Shark.common.name',  # Display shark name on hover
            center=dict(lat=-28, lon=130),
            zoom=2.5,
            mapbox_style="open-street-map",
            labels={selected_var: categories[selected_var]},
            color_discrete_sequence = px.colors.qualitative.Light24 # changes colourmap
        )
        map_fig.update_traces(marker=dict(size=8)) # changes dot size
        map_fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))


    # Create the bar chart figure
    switch_bar1 = n_clicks_bar1 % 2 == 1
    bar1_x, bar1_y = (selected_var, 'Count') if not switch_bar1 else ('Count', selected_var)
    activity_counts = filtered_df[selected_var].value_counts().reset_index()
    activity_counts.columns = [selected_var, 'Count']
    activity_counts['Shortened'] = activity_counts[selected_var].astype(str).str[:10]  # Use first 10 characters
    bar1_x, bar1_y = ('Shortened', 'Count') if not switch_bar1 else ('Count', 'Shortened')
    bar_fig = px.bar(
        activity_counts,
        x=bar1_x,
        y=bar1_y,
        labels={'Shortened': categories[selected_var], "Count": "Count"},
    )
    bar_fig.update_layout(margin=dict(l=5, r=5, t=40, b=5))

    # Create the second bar chart figure
    switch_bar2 = n_clicks_bar2 % 2 == 1
    bar2_x, bar2_y = (selected_var2, 'Count') if not switch_bar2 else ('Count', selected_var2)
    activity_counts2 = filtered_df[selected_var2].value_counts().reset_index()
    activity_counts2.columns = [selected_var2, 'Count']
    activity_counts2['Shortened'] = activity_counts2[selected_var2].astype(str).str[:10]  # Use first 10 characters
    bar2_x, bar2_y = ('Shortened', 'Count') if not switch_bar2 else ('Count', 'Shortened')
    bar_fig2 = px.bar(
        activity_counts2,
        x=bar2_x,
        y=bar2_y,
        labels={'Shortened': categories[selected_var2], "Count": "Count"},
    )
    bar_fig2.update_layout(margin=dict(l=5, r=5, t=40, b=5))

    # # Create the heatmap figure
    # heat_fig = px.density_heatmap(
    #     filtered_df,
    #     x=selected_var,
    #     y=selected_var2,
    #     labels={selected_var: categories[selected_var], selected_var2: categories[selected_var2]},
    #     text_auto=True,
    # )

    heat_fig = go.Figure(go.Histogram2d(
        x=filtered_df[selected_var],
        y=filtered_df[selected_var2],
        # legend={selected_var: categories[selected_var2], selected_var2: categories[selected_var2]},
    ))
    heat_fig.update_layout(margin=dict(l=5, r=5, t=40, b=5))

    # create the timeline histogram
    timeline_fig = px.histogram(
        filtered_df,
        x="Incident.date",
        nbins=100,
        height=200,
        title="Timeline of Incidents",
        labels={"Incident.date": "", "count": "Frequency"},
    )
    timeline_fig.update_layout(margin=dict(l=10, r=50, t=60, b=5))

    return map_fig, bar_fig, bar_fig2, heat_fig, timeline_fig, row_details

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
        ["include"],
        [year_min, year_max]
    )

@app.callback(
    Output("modal-dismiss", "is_open"),
    [Input("open-dismiss", "n_clicks"), Input("close-dismiss", "n_clicks")],
    [State("modal-dismiss", "is_open")],
)
def toggle_modal(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
