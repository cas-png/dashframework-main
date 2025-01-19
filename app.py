"""
This module initializes a Dash web application for visualizing shark incident data. 
It provides various interactive components such as dropdowns, sliders, and buttons 
to filter and visualize the data through maps, bar charts, and heatmaps.
The main components of the module include:
- Loading the data.
- Defining the layout of the Dash app, including sidebars, main content areas, and various interactive elements.
- Creating callbacks to update the visualizations based on user interactions.
- Providing options to reset filters and selections.
- Displaying additional information through a pop-up modal.
The visualizations include:
- A scatter plot or heatmap of shark incidents on a map.
- Bar charts showing distributions of selected variables.
- A heatmap showing correlations between selected variables.
- A timeline histogram of incidents over time.
The module uses the following libraries:
- Dash for creating the web application and interactive components.
- Plotly for creating visualizations.
- Pandas and NumPy for data manipulation.
- Dash Bootstrap Components for styling.
"""
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from jbi100_app.data import get_data


# Load the data
df = get_data()

# Initialize the Dash app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Get the range of shark lengths for the slider
shark_length_min = df['Shark.length.m'].min()
shark_length_max = df['Shark.length.m'].max()

# Get the range of years for the year slider
year_min = df['Incident.year'].min()
year_max = df['Incident.year'].max()

# Define for each category a human-readable name
categories = {'Incident.month': 'Incident Month',
              'Injury.severity': 'Victim Injury Severity', 
              'Victim.injury': 'Victim Injury Result', 
              'State': 'State', 
              'Site.category': 'Location Type', 
              'Shark.common.name': 'Shark Type',
              'Provoked/unprovoked': 'Provoked', 
              'Victim.activity': 'Victim Activity',
              'Victim.gender': 'Victim Gender',
              'Data.source': 'Source Type'}

# Overview of the variables shown in the tool and the columns from the data source that are used in that variable, used for the pop-up modal
category_info = {'Incident Date': 'Based on Incident.year and Incident.month',
                 'Victim Injury Severity': 'Injury.severity', 
                 'Victim Injury Result': 'Victim.injury', 
                 'State': 'State', 
                 'Location Type': 'Site.category', 
                 'Shark Type': 'Shark.common.name',
                 'Provoked': 'Provoked/unprovoked', 
                 'Victim Activity': 'Victim.activity',
                 'Victim Gender': 'Victim.gender',
                 'Source Type': 'Data.source',
                 'Shark Length': 'Shark.length.m'}

# Define the continuous color scales
colorscales = px.colors.named_colorscales()
# Define the discrete color palettes
colorsequences = {
    'Alphabet': px.colors.qualitative.Alphabet,
    'Antique': px.colors.qualitative.Antique,
    'Bold': px.colors.qualitative.Bold,
    'Dark24': px.colors.qualitative.Dark24,
    'Dark2': px.colors.qualitative.Dark2,
    'Light24': px.colors.qualitative.Light24,
    'Pastel': px.colors.qualitative.Pastel,
    'Pastel1': px.colors.qualitative.Pastel1,
    'Pastel2': px.colors.qualitative.Pastel2,
    'Safe': px.colors.qualitative.Safe,
    'Set1': px.colors.qualitative.Set1,
    'Set2': px.colors.qualitative.Set2,
    'Set3': px.colors.qualitative.Set3,
    'Vivid': px.colors.qualitative.Vivid
}

##### Create the layout #####

# Full-screen container
app.layout = html.Div(style={'height': '98vh', 'width': '98vw', 'margin': 0, 'padding': 0, 'display': 'flex'}, children=[
    # Sidebar with dropdown and filters
    html.Div(style={'width': '15%', 'padding': '10px', 'float': 'left', 'border': '1px solid rgba(0, 0, 0, 1)', 'fontSize': '12px', 'overflow-y': 'scroll'}, children=[
        # Dropdown for selecting shark type: Shark.common.name
        html.Label('Shark Type:'),
        dcc.Dropdown(
            id='shark-dropdown',
            options=[{'label': shark, 'value': shark} for shark in df['Shark.common.name'].unique()],
            multi=True,
            placeholder='Select shark type(s)',
            style={'fontSize': '12px', 'maxHeight': '100px'}
        ),
        # Dropdown for selecting victim injury result: Victim.injury
        html.Label('Victim Injury Result:'),
        dcc.Dropdown(
            id='injury-dropdown',
            options=[{'label': level, 'value': level} for level in df['Victim.injury'].unique()],
            multi=True,
            placeholder='Select injury result(s)',
        ),
        # Dropdown for selecting injury severity: Injury.severity
        html.Label('Victim Injury Severity:'),
        dcc.Dropdown(
            id='injury-severity-dropdown',
            options=[{'label': level, 'value': level} for level in df['Injury.severity'].unique()],
            multi=True,
            placeholder='Select injury severity(s)',
        ),
        # Dropdown for selecting state: State
        html.Label('State:'),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': level, 'value': level} for level in df['State'].unique()],
            multi=True,
            placeholder='Select state(s)',
        ),
        # Dropdown for selecting location type: Site.category
        html.Label('Location Type:'),
        dcc.Dropdown(
            id='site-dropdown',
            options=[{'label': level, 'value': level} for level in df['Site.category'].unique()],
            multi=True,
            placeholder='Select state(s)',
        ),
        # Dropdown for selecting victim gender: Victim.gender
        html.Label('Victim Gender:'),
        dcc.Dropdown(
            id='gender-dropdown',
            options=[{'label': level, 'value': level} for level in df['Victim.gender'].unique()],
            multi=True,
            placeholder='Select gender(s)',
        ),
        # Dropdown for selecting data source: Data.source
        html.Label('Data Source:'),
        dcc.Dropdown(
            id='source-dropdown',
            options=[{'label': level, 'value': level} for level in df['Data.source'].unique()],
            multi=True,
            placeholder='Select source(s)',
        ),
        # Dropdown for selecting victim activity: Victim.activity
        html.Label('Victim Activity:'),
        dcc.Dropdown(
            id='victim-activity-dropdown',
            options=[{'label': level, 'value': level} for level in df['Victim.activity'].unique()],
            multi=True,
            placeholder='Select activity(s)',
        ),
        # Dropdown for provoked status: Provoked/unprovoked
        html.Label('Provoked Status:'),
        dcc.Dropdown(
            id='provoked-status',
            options=[{'label': level, 'value': level} for level in df['Provoked/unprovoked'].unique()],
            multi=True,
            placeholder='Select provoked status',
        ),
        html.Br(), # Add a line break
        # Range slider for shark length: Shark.length.m
        html.Label('Shark Length (meters):'),
        dcc.RangeSlider(
            id='shark-length-slider',
            min=shark_length_min,
            max=shark_length_max,
            step=0.1,
            marks ={0.3: '0.3', 1.4: '1.4', 2.6: '2.6', 3.7: '3.7', 4.9: '4.9', 6: '6.0'}, # based on np.linspace(shark_length_min, shark_length_max, num=6) but now 6.0 shows up
            value=[shark_length_min, shark_length_max],
            tooltip={'placement': 'bottom', 'always_visible': False},
        ),
        html.Br(), # Add a line break
        # Checkbox for including unknown lengths
        dcc.Checklist(
            id='include-unknown-length',
            options=[{'label': ' Include unknown lengths', 'value': 'include'}],
            value=['include']
        ),
        html.Br(), # Add a line break
        # Reset filters button
        html.Button(
            'Reset Filters',
            id='reset-filters-button',
        ),
        # Reset selection button
        html.Button(
            'Reset Selection',
            id='reset-selection-button',
        ),
        html.Br(), # Add a line break
        html.Div(id='row-details'), # Display the number and percentage of rows in the filtered and selected data
        html.Br(), # Add a line break
        # Dropdown for selecting continuous color palette/colorscale
        html.Label('Select Continuous Color Palette:'),
        dcc.Dropdown(
            id='color-dropdown',
            options=colorscales,
            value='viridis',
            clearable=False
        ),
        # Dropdown for selecting discrete color palette
        html.Label('Select Discrete Color Palette:'),
        dcc.Dropdown(
            id='color-dropdown-discrete',
            options=list(colorsequences.keys()),
            value='Vivid',
            clearable=False
        ),
        html.Br(), # Add a line break
        # Pop-up modal for extra info
        dbc.Button('Info', id='open-dismiss'), # Button to open the modal
        dbc.Modal(
            [
                dbc.ModalHeader( # Header of the modal
                    dbc.ModalTitle('Tool and Data Information'), close_button=False
                ),
                dbc.ModalBody(children=[ # Body of the modal: information and links to information and code from the tool and data, and a table with variable details
                    html.Div('The table below lists each variable shown in the tool and provides the columns from the data source that are used in that variable.'),
                    dash_table.DataTable([{'Variable Name': key, 'Details': value} for key, value in category_info.items()]),
                    html.Div('Tool created by JBI100 team 30 (2024 Q2).'),
                    dbc.Button('Visualisation Tool GitHub', href='https://github.com/cas-png/dashframework-main'),
                    dbc.Button('Data Source GitHub', href='https://github.com/cjabradshaw/AustralianSharkIncidentDatabase'),
                    dbc.Button('Video Presentation', href='/'),
            ]),
                dbc.ModalFooter(dbc.Button('Close', id='close-dismiss'), className='justify-content-center') # Footer of the modal: close button
            ],
            id='modal-dismiss',
            fullscreen=True,
        ),
    ]),

    # Main content with map and timeline and year range slider
    html.Div(style={'width': '45%', 'display': 'flex', 'flexDirection': 'column'}, children=[
        # Tabs for switching between heatmap and scatter plot
        dcc.Tabs(
            id='map-tabs',
            value='scatter',  # Default tab
            children=[
                dcc.Tab(label='Scatter Plot', value='scatter'),
                dcc.Tab(label='Heatmap', value='heatmap'),
            ],
        ),
        # Map and timeline and year range slider
        html.Div(style={'display': 'flex', 'flexDirection': 'column', 'height': '100%'}, children=[
            # Map
            html.Div(style={'display': 'flex', 'height': '65%', 'width': '100%'}, children=[dcc.Graph(id='shark-map', style={'width': '100%', 'height': '100%'}, config={'scrollZoom': True})]),
            # Timeline
            html.Div(style={'display': 'flex', 'height': '25%', 'width': '100%'}, children=[dcc.Graph(id='timeline', style={'width': '100%', 'height': '100%'})]),
            # Year Range Slider below the map
            html.Label(id='slider-label'),  # Create a label for dynamic updates
            dcc.RangeSlider(
                id='year-slider',
                min=year_min,
                max=year_max,
                step=1,
                marks={year: str(int(year)) for year in range(year_min, year_max+1, 20)},
                value=[year_min, year_max],
                tooltip={'placement': 'bottom', 'always_visible': False}, # Enable tooltip
                allowCross=False,
                dots=False
            ),
        ]),
    ]),

    # Bar charts for distributions and heat map
    html.Div(style={'width': '40%', 'padding': '10px', 'border': '1px solid rgba(0, 0, 0, 1)', 'display': 'flex', 'flexDirection': 'column'}, children=[
        # Dropdown for selecting variable for bar chart 1 and the map
        dcc.Dropdown(
            id='var-select',
            options=[
                {'label': categories[category], 'value': category} for category in categories
            ],
            placeholder='Select a variable',
            value='Victim.injury',
            clearable=False
        ),
        # Dropdown for selecting variable for bar chart 2
        dcc.Dropdown(
            id='var-select2',
            options=[
                {'label': categories[category], 'value': category} for category in categories
            ],
            placeholder='Select a variable',
            value='Provoked/unprovoked',
            clearable=False
        ),
        # Buttons to switch axes for the bar charts
        html.Div([
            html.Button('Switch Axes for Bar Chart 1', id='switch-axes-bar1', n_clicks=0),
            html.Button('Switch Axes for Bar Chart 2', id='switch-axes-bar2', n_clicks=0),
            ], style={'display': 'flex', 'justify-content': 'space-between', 'margin': '10px 0'}
        ),
        # Bar charts
        html.Div(style={'display': 'flex', 'flexDirection': 'row', 'flex': '1', 'width': '100%', 'height': '40%'}, children=[
            dcc.Graph(id='activity-bar-chart', style={'flex': '1', 'width': '100%', 'height': '100%'}),
            dcc.Graph(id='activity-bar-chart2', style={'flex': '1', 'width': '100%', 'height': '100%'}),
        ]),
        # Heatmap
        html.Div(style={'display': 'flex', 'flexDirection': 'column', 'width': '100%', 'height': '40%'}, children=[
            dcc.Graph(id='heat-chart', style={'flex': '1', 'width': '100%', 'height': '100%'})
        ])
    ]),
])

##### Create the callbacks #####

# Callback to update: map, bar charts, heat map, timeline, and row details
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
        Input('switch-axes-bar2', 'n_clicks'),
        Input('shark-map', 'selectedData'),
        Input('color-dropdown', 'value'),
        Input('color-dropdown-discrete', 'value'),
    ]
)
def update_map_and_chart(selected_sharks, selected_injuries, selected_injury_severities, selected_activities, selected_sources, selected_genders, selected_sites, selected_states, shark_length_range, provoked_status, include_unknown_length, selected_tab, year_range, selected_var, selected_var2, n_clicks_bar1, n_clicks_bar2, selected_data, color_palette, color_sequence):
    """
        Update the map and charts based on the selected filters and parameters.
        Args:
        - selected_sharks (list): List of selected shark types.
        - selected_injuries (list): List of selected injury levels.
        - selected_injury_severities (list): List of selected injury severities.
        - selected_activities (list): List of selected activities.
        - selected_sources (list): List of selected data sources.
        - selected_genders (list): List of selected genders.
        - selected_sites (list): List of selected sites.
        - selected_states (list): List of selected states.
        - shark_length_range (tuple): Range of selected shark lengths.
        - provoked_status (list): List of selected provoked statuses.
        - include_unknown_length (str): Option to include unknown shark lengths.
        - selected_tab (str): Selected tab for map visualization ('heatmap' or 'scatter').
        - year_range (tuple): Range of selected years.
        - selected_var (str): First variable selected for visualization.
        - selected_var2 (str): Second variable selected for visualization.
        - n_clicks_bar1 (int): Number of clicks for the first bar chart.
        - n_clicks_bar2 (int): Number of clicks for the second bar chart.
        - selected_data (dict): Data selected on the map.
        - color_palette (str): Color palette for the heatmap.
        - color_sequence (str): Color sequence for the scatter plot.
        Returns:
        - map_fig (plotly.graph_objs._figure.Figure): Map figure (heatmap or scatter plot).
        - bar_fig (plotly.graph_objs._figure.Figure): First bar chart figure.
        - bar_fig2 (plotly.graph_objs._figure.Figure): Second bar chart figure.
        - heat_fig (plotly.graph_objs._figure.Figure): Correlation heatmap figure.
        - timeline_fig (plotly.graph_objs._figure.Figure): Timeline histogram figure.
        - row_details (str): Details about the number and percentage of rows in filtered and selected data.
        """

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
    # Filter the data based on the selected shark length range
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
    # Filter the data based on the selected provoked status(es)
    if provoked_status:
        filtered_df = filtered_df[filtered_df['Provoked/unprovoked'].isin(provoked_status)]
    # Filter the data based on the selected year range
    filtered_df = filtered_df[
        (filtered_df['Incident.year'] >= year_range[0]) &
        (filtered_df['Incident.year'] <= year_range[1])
    ]

    # Create selected_df based on selected_data
    if selected_data and selected_data['points']:
        selected_coords = [(point['lat'], point['lon']) for point in selected_data['points']]
        selected_latitudes, selected_longitudes = zip(*selected_coords)
        selected_df = filtered_df[
            filtered_df['Latitude'].isin(selected_latitudes) &
            filtered_df['Longitude'].isin(selected_longitudes)
            ]
        filtered_df = filtered_df.assign(IsSelected=filtered_df['index1'].isin(selected_df['index1'])) # Create a new column to indicate selected rows
        filtered_df = filtered_df.assign(Size=filtered_df['IsSelected'].astype(float).apply(lambda x: 1 if x == 1 else 0.3)) # Create a new column to indicate map marker size based on selection
    else:
        selected_df = pd.DataFrame(columns=filtered_df.columns)  # Empty DataFrame if nothing is selected
        filtered_df['IsSelected'] = True # Create a new column to indicate selected rows (none, so all rows are fake selected)
        filtered_df['Size'] = 1.0  # Create a new column to indicate map marker size based on selection (none, so all markers are full size)

    # Calculate row details (number and percentage of rows in filtered and selected data)
    filtered_row_percentage = np.round(len(filtered_df) / len(df) * 100, 2)
    selected_row_percentage = np.round(len(selected_df) / len(df) * 100, 2)
    row_details = (
        f'Filtered Data: {len(filtered_df)} rows ({filtered_row_percentage}% of total rows). '
        f'Selected Data: {len(selected_df)} rows ({selected_row_percentage}% of total rows).'
    )

    # Create the map figure
    if selected_tab == 'heatmap':
        # Create density map (heatmap)
        map_fig = px.density_mapbox(
            filtered_df,
            lat='Latitude',
            lon='Longitude',
            radius=5,
            center=dict(lat=-28, lon=130), # Roughly the center of Australia
            zoom=2.5,
            mapbox_style='open-street-map',
            color_continuous_scale=color_palette, # Changes colourmap
        )
        map_fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))
    else:  # selected_tab == 'scatter'
        # Create scatter plot map
        map_fig = px.scatter_map(
            filtered_df,
            lat='Latitude',
            lon='Longitude',
            color=selected_var,  # Color by incident type
            size='Size', # comment out to fix
            center=dict(lat=-28, lon=130),
            zoom=2.5,
            map_style='open-street-map',
            hover_name='Shark.full.name',  # Display shark name on hover
            hover_data={selected_var: True, selected_var2: True, 'Size': False, 'IsSelected': True, 'Latitude': True, 'Longitude': True},
            labels={selected_var: categories[selected_var], selected_var2: categories[selected_var2], 'IsSelected': 'Selected'},
            color_discrete_sequence = colorsequences[color_sequence], # changes colourmap
            size_max=8, # Maximum marker size
            opacity=1,
        )
        map_fig.update_layout(margin=dict(l=5, r=5, t=30, b=5))

    # Combine the filtered and selected data for the first bar chart with a new column 'Source'
    combined_df = (
        pd.concat([
            filtered_df[[selected_var]].assign(Source='Filtered Data'),
            selected_df[[selected_var]].assign(Source='Selected Data')
        ])
        .groupby([selected_var, 'Source'])
        .size()
        .reset_index(name='Count')
    )
    # Switch axes for the first bar chart
    switch_bar1 = n_clicks_bar1 % 2 == 1
    bar1_x, bar1_y = (selected_var, 'Count') if not switch_bar1 else ('Count', selected_var)
    # Generate the first bar chart for filtered_df and selected_df
    bar_fig = px.bar(
        combined_df,
        x=bar1_x,
        y=bar1_y,
        color='Source',
        barmode='group',
        labels={selected_var: categories[selected_var], 'Count': 'Count', 'Source': 'Data Source'},
    )
    bar_fig.update_layout(
        margin=dict(l=5, r=5, t=40, b=5),  # Adjust margins as needed
        legend=dict(
            orientation='h',  # Horizontal legend
            yanchor='top',
            y=1,  # Inside the chart at the top
            xanchor='center',
            x=0.5,  # Centered horizontally
            font=dict(size=10),  # Smaller font size
            bgcolor='rgba(255, 255, 255, 0.3)',  # Semi-transparent background for better readability
        )
    )

    # Combine the filtered and selected data for the second bar chart with a new column 'Source'
    combined_df2 = (
        pd.concat([
            filtered_df[[selected_var2]].assign(Source='Filtered Data'),
            selected_df[[selected_var2]].assign(Source='Selected Data')
        ])
        .groupby([selected_var2, 'Source'])
        .size()
        .reset_index(name='Count')
    )
    # Switch axes for the second bar chart
    switch_bar2 = n_clicks_bar2 % 2 == 1
    bar2_x, bar2_y = (selected_var2, 'Count') if not switch_bar2 else ('Count', selected_var2)
    # Generate the second bar chart for filtered_df and selected_df
    bar_fig2 = px.bar(
        combined_df2,
        x=bar2_x,
        y=bar2_y,
        color='Source',
        barmode='group',
        labels={selected_var2: categories[selected_var2], 'Count': 'Count', 'Source': 'Data Source'},
    )
    bar_fig2.update_layout(
        margin=dict(l=5, r=5, t=40, b=5),  # Adjust margins as needed
        legend=dict(
            orientation='h',  # Horizontal legend
            yanchor='top',
            y=1,  # Inside the chart at the top
            xanchor='center',
            x=0.5,  # Centered horizontally
            font=dict(size=10),  # Smaller font size
            bgcolor='rgba(255, 255, 255, 0.3)',  # Semi-transparent background for better readability
        )
    )

    # Create correlation heatmap
    filtered_df['Modified_var'] = filtered_df[selected_var].astype(str).str.replace('shark', '', regex=False)
    filtered_df['Modified_var2'] = filtered_df[selected_var2].astype(str).str.replace('shark', '', regex=False)
    heat_fig = go.Figure(go.Histogram2d(
        x=filtered_df['Modified_var'],
        y=filtered_df['Modified_var2'],
        # legend={selected_var: categories[selected_var2], selected_var2: categories[selected_var2]},
        colorscale=color_palette,  # changes colourmap
        texttemplate='%{z}',
    ))
    heat_fig.update_layout(margin=dict(l=5, r=5, t=40, b=5))

    # create the timeline histogram
    timeline_fig = px.histogram(
        filtered_df,
        x='Incident.date',
        nbins=100,
        height=200,
        title='Timeline of Incidents',
        labels={'Incident.date': '', 'count': 'Frequency'},
    )
    timeline_fig.update_layout(margin=dict(l=10, r=50, t=60, b=5))

    return map_fig, bar_fig, bar_fig2, heat_fig, timeline_fig, row_details

# Callback to reset filters
@app.callback(
    [
        Output('shark-dropdown', 'value'),
        Output('injury-dropdown', 'value'),
        Output('injury-severity-dropdown', 'value'),
        Output('state-dropdown', 'value'),
        Output('site-dropdown', 'value'),
        Output('gender-dropdown', 'value'),
        Output('source-dropdown', 'value'),
        Output('victim-activity-dropdown', 'value'),
        Output('shark-length-slider', 'value'),
        Output('provoked-status', 'value'),
        Output('include-unknown-length', 'value'),
        Output('year-slider', 'value'),
        Output('color-dropdown', 'value'),
        Output('color-dropdown-discrete', 'value')
    ],
    Input('reset-filters-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    """
    Resets all filter components to their default values.
    
    Args:
    - n_clicks (int): The number of times the reset button has been clicked.
    Returns:
    - tuple: A tuple containing the default values for all filter components.
    """
    return (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        [shark_length_min, shark_length_max],
        None,
        ['include'],
        [year_min, year_max],
        'viridis',
        'Vivid'
    )

# Callback to reset selection
@app.callback(
    [Output('shark-map', 'selectedData')],
    Input('reset-selection-button', 'n_clicks'),
    prevent_initial_call=True
)
def reset_selection(n_clicks):
    """
    Resets the selection based on the number of clicks.
    Args:
    - n_clicks (int): The number of clicks that triggers the reset.
    Returns:
    - list: A list containing a single None element, indicating the reset state.
    """
    return [None]

# Callback to toggle the pop-up modal
@app.callback(
    Output('modal-dismiss', 'is_open'),
    [Input('open-dismiss', 'n_clicks'), Input('close-dismiss', 'n_clicks')],
    [State('modal-dismiss', 'is_open')],
)
def toggle_modal(n_open, n_close, is_open):
    """
    Toggles the state of the pop-up modal window.
    
    Args:
    - n_open (int): The number of times the open button has been clicked.
    - n_close (int): The number of times the close button has been clicked.
    - is_open (bool): The current state of the modal window (True if open, False if closed).
    Returns:
    - bool: The new state of the modal window (True if it should be open, False if it should be closed).
    """
    if n_open or n_close:
        return not is_open
    return is_open

# Run the server
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=True) # set debug True to get errors and issues on the webpage with that blue circle
