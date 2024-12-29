from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from jbi100_app.data import get_data

# Load the data
df = get_data()

# Initialize the Dash app
app = Dash()

# Layout
app.layout = html.Div(style={'display': 'flex', 'height': '100vh'}, children=[
    html.Div(style={'width': '10%', 'padding': '10px', 'background-color': '#f9f9f9', 'float': 'left'}, children=[
        # html.H3("Map View - Shark Attacks", style={'textAlign': 'center'}),
        html.H3("Filters", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='shark-filter',
            options=[{'label': shark, 'value': shark} for shark in df['Shark.common.name'].unique()],
            placeholder="Select shark type",
            multi=True  # Allow multiple shark types to be selected
        ),
        dcc.Dropdown(
            id='injury-filter',
            options=[{'label': injury, 'value': injury} for injury in df['Victim.injury'].unique()],
            placeholder="Select injury severity",
            multi=True  # Allow multiple injury severities to be selected
        )
    ]),
    html.Div(style={'width': '60%', 'padding': '10px'}, children=[
        dcc.Graph("map", style={'textAlign': 'center'},
        clickData=None),

        dcc.RangeSlider(
            id='year-filter',
            min=df['Incident.year'].min(),
            max=df['Incident.year'].max(),
            step=1,
            marks={year: str(year) for year in range(df['Incident.year'].min(), df['Incident.year'].max() + 1, 10)},
            # Marks every 5 years
            value=[df['Incident.year'].min(), df['Incident.year'].max()],
            tooltip={"placement": "bottom", "always_visible": True},
            verticalHeight=5)
    ]),
    html.Div(style={'width': '30%', 'padding': '10px', 'background-color': '#f3f3f3'}, children=[
        html.H3("Future Graphs", style={'textAlign': 'center'}),
        dcc.Graph(
            id="line-graph",
            style={'textAlign': 'center', 'height': '50%'})
    ])
])



# Callback to update the map based on filters
@app.callback(
    [Output('map', 'figure'),
     Output('line-graph', 'figure')],
    [Input('shark-filter', 'value'),
     Input('injury-filter', 'value'),
     Input('map', 'clickData'),
     Input('year-filter', 'value')
])


def update_map(selected_sharks, selected_injury, clickData, selected_years):
    # Filter data based on selected shark type and injury severity
    filtered_df = df

    # If no sharks selected, keep all
    if selected_sharks:
        filtered_df = filtered_df[filtered_df['Shark.common.name'].isin(selected_sharks)]

    # If no injury types selected, keep all
    if selected_injury:
        filtered_df = filtered_df[filtered_df['Victim.injury'].isin(selected_injury)]

    filtered_df = filtered_df[
        (filtered_df['Incident.year'] >= selected_years[0]) &
        (filtered_df['Incident.year'] <= selected_years[1])]

    if clickData:
        # Extract the shark name from the clicked point
        clicked_shark = clickData['points'][0]['customdata'][0]

        # Update the shark filter to only show the clicked shark
        selected_sharks = [clicked_shark]  # Automatically filter for the clicked shark

        # Filter data to only include the clicked shark
        filtered_df = filtered_df[filtered_df['Shark.common.name'] == clicked_shark]

        if filtered_df.empty:
            filtered_df = df

    # Map view
    map_fig = px.scatter_geo(
        filtered_df,
        lat='Latitude',
        lon='Longitude',
        color='Victim.injury',  # Use 'Victim.injury' for the color
        title="Shark Attacks in Australia",
        hover_data={'Incident.year': True, 'Shark.common.name': True, 'Victim.injury': True}
    )

    map_fig.update_geos(fitbounds="locations")  # Zoom into points

    if selected_sharks:
        # Group by year and count the number of shark attacks (data points) for each year
        line_df = filtered_df.groupby('Incident.year').size().reset_index(name='Attack Count')
        line_fig = px.line(
            line_df,
            x='Incident.year',
            y='Attack Count',
            title='Number of Shark Attacks per Year',
            labels={'Incident.year': 'Year', 'Attack Count': 'Number of Attacks'}
        )
    else:
        line_fig = {}

    return map_fig, line_fig


# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
