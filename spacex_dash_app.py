# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                             ],
                                             value='All',
                                             placeholder='Select Launch Site',
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    #  [Output(component_id='site-name', component_property='value')],
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_value):
    if entered_value == 'ALL':
        launch_sites_df = spacex_df.groupby('Launch Site').sum()['class'].reset_index()
        launch_sites_df.rename(columns={'class': 'success launches'}, inplace=True)
        fig = px.pie(launch_sites_df, values='success launches', names='Launch Site',
                     title='Successful Launches from All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_value]
        result_df = filtered_df['class'].value_counts().reset_index()
        result_df = result_df.rename(columns={'index': 'success'})
        fig = px.pie(result_df, values='class', names='success', title='Outcome ' + entered_value)
    # if entered_value == 'KSC LC-39A':
    #     filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
    #     result_df = filtered_df['class'].value_counts().reset_index()
    #     result_df = result_df.rename(columns={'index': 'success'})
    #     fig = px.pie(result_df, values='class', names='success', title='Outcome ' + entered_value)
    # elif entered_value == 'VAFB SLC-4E':
    #     filtered_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
    #     result_df = filtered_df['class'].value_counts().reset_index()
    #     result_df = result_df.rename(columns={'index': 'success'})
    #     fig = px.pie(result_df, values='class', names='success', title='Outcome ' + entered_value)
    # elif entered_value == 'CCAFS SLC-40':
    #     filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
    #     result_df = filtered_df['class'].value_counts().reset_index()
    #     result_df = result_df.rename(columns={'index': 'success'})
    #     fig = px.pie(result_df, values='class', names='success', title='Outcome ' + entered_value)
    # elif entered_value == 'CCAFS LC-40':
    #     filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
    #     result_df = filtered_df['class'].value_counts().reset_index()
    #     result_df = result_df.rename(columns={'index': 'success'})
    #     fig = px.pie(result_df, values='class', names='success', title='Outcome ' + entered_value)
    # else:
    #     launch_sites_df = spacex_df.groupby('Launch Site').sum()['class'].reset_index()
    #     launch_sites_df.rename(columns={'class': 'success launches'}, inplace=True)
    #     fig = px.pie(launch_sites_df, values='success launches', names='Launch Site',
    #                  title='Successful Launches from All Sites')
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_value, entered_range):
    low_range = entered_range[0]
    high_range = entered_range[1]
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low_range) & (spacex_df['Payload Mass (kg)'] <= high_range)]
    if entered_value == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",
                         title='All Sites Success by Payload and Booster Version')
    else:
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == entered_value]
        fig = px.scatter(site_filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",
                         title=entered_value + 'Success by Payload and Booster Version')

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
