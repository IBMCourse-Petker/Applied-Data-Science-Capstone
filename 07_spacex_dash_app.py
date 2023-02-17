#%% Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

#%% Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
spacex_df.head()


# Create a dash application
app = dash.Dash(__name__)

# Dropdown options
options = [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
options = [{'label': site, 'value': site} for site in ['All Sites'] + list(spacex_df['Launch Site'].unique())]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=options, value='All Sites',
                                placeholder='Select a Launch Site', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=min_payload,
                                max=max_payload,
                                value=[min_payload, max_payload],
                                marks={str(payload): str(payload) for payload in spacex_df['Payload Mass (kg)'].unique()}),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.Br(),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def piegraph_update(site_dropdown):
    if site_dropdown == 'All Sites' or site_dropdown == 'None':
        data  = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(data, names = 'Launch Site', title = 'Total Success Launches by Site')
    else:
        data = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(data, names = 'class', title = 'Total Success Launches for Site ' + site_dropdown,)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'),
              Input('site-dropdown', 'value'),
              Input('payload-slider', 'value'))
def update_scatter_chart(site, payload):
    if site == 'All Sites':
        df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1])]
        title = f'Success Launches for All Sites with Payload Range: {payload[0]} - {payload[1]} kg'
    else:
        df = spacex_df[(spacex_df['Launch Site'] == site) & (spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1])]
        title = f'Success Launches for {site} with Payload Range: {payload[0]} - {payload[1]} kg'
    fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title=title)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
