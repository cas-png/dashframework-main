from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from jbi100_app.data import get_data

# Load the data
df = get_data()

# Initialize the Dash app
app = Dash()

tabs_=dcc.Tabs(
        id="map-tabs",
        value="heatmap",  # Default tab
        children=[
            dcc.Tab(label="Heatmap", value="heatmap"),
            dcc.Tab(label="Scatter Plot", value="scatter"),
        ],
    )
map_=dcc.Graph(
        id='shark-map',
        style={"flex": "3", "marginRight": "10px"}
    )
bar_chart_=dcc.Graph(
        id='activity-bar-chart',
        style={"flex": "1"}
    )
timeline_chart_=dcc.Graph(
        id='timeline-chart',
        style={"flex": "1"}
    )

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
                    placeholder="Select a variable",
                ),
            ],
        ),
        # Main content with map and bar chart
        html.Div(
            style={"width": "80%", "display": "flex", "flexDirection": "column", "padding": "10px"},
            children=[
                tabs_,
                html.Div(
                    style={"display": "flex", "flexDirection": "row", "height": "100%"},
                    children=[
                        html.Div(
                            style={"display": "flex", "flexDirection": "column", "height": "100%", "width": "70%"},
                            children=[
                                map_,
                                timeline_chart_,
                            ]
                        ),
                        html.Div(
                            style={"display": "flex", "flexDirection": "column", "height": "100%", "width": "30%"},
                            children=[
                                bar_chart_,
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ]
)


# Callback to update the map and bar chart
@app.callback(
    [Output('shark-map', 'figure'),
     Output('activity-bar-chart', 'figure'),
     Output('timeline-chart', 'figure')],
    [Input('shark-dropdown', 'value'),
     Input('map-tabs', 'value'),
     Input('var-select', 'value'),]
)

def callback(selected_shark, selected_tab, selected_var='Victim.activity'):
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
    else:# selected_tab == "scatter":
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
    bar_fig = px.histogram(
        activity_counts,
        x=selected_var,
        y='Count',
        title="Distribution of"+selected_var,
        nbins=20,
        labels={selected_var: "activity Type", "Count": "Count"},
    )

    # Create the bar chart figure
    timeline_counts = filtered_df['Incident.date'].value_counts().reset_index()
    timeline_counts.columns = ['Incident.date', 'Count']
    timeline_fig = px.bar(
        timeline_counts,
        x='Incident.date',
        range_x=[df['Incident.date'].min(), df['Incident.date'].max()],
        y='Count',
        title="Distribution of incidents over time",
        # nbins=filtered_df['Incident.year'].unique().shape[0],
        labels={"Incident.date": "Month of indicent", "Count": "Count"},
    )
    timeline_fig.update_xaxes(
        rangeslider_visible=True,
        tickformatstops = [
            dict(dtickrange=[None, "M12"], value="%b '%y"),
            dict(dtickrange=["M12", None], value="%Y")
        ],
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                    label="1m",
                    step="month",
                    stepmode="backward"),
                dict(count=6,
                    label="6m",
                    step="month",
                    stepmode="backward"),
                dict(count=1,
                    label="YTD",
                    step="year",
                    stepmode="todate"),
                dict(count=1,
                    label="1y",
                    step="year",
                    stepmode="backward"),
                dict(step="all")
            ])
        ),
    )

    return map_fig, bar_fig, timeline_fig

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
