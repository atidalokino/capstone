# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the data
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard'),
    
    # Dashboard 1: Launch Site
    html.Div([
        html.Label('Select a launch site:'),
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
            ],
            value='CCAFS SLC-40'
        ),
        dcc.Graph(id='success-pie-chart')
    ]),
    
    # Dashboard 2: Payload
    html.Div([
        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id='payload-slider',
            min=spacex_df['Payload Mass (kg)'].min(),
            max=spacex_df['Payload Mass (kg)'].max(),
            value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()],
            step=100
        ),
        dcc.Graph(id='payload-scatter-chart')
    ]),
    
    # Dashboard 3: Launch Success
    html.Div([
        dcc.Graph(id='success-bar-chart')
    ]),
    
    # Dashboard 4: Correlation
    html.Div([
        dcc.Graph(id='correlation-scatter-chart')
    ])
])

# Define the callbacks
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def render_success_pie_chart(selected_site):
    filtered_data = spacex_df[spacex_df['Launch Site'] == selected_site]
    success_counts = filtered_data['class'].value_counts()
    fig = px.pie(values=success_counts.values, names=success_counts.index, title='Success Rate by Launch Site')
    return fig

@app.callback(
    Output('payload-scatter-chart', 'figure'),
    [Input('payload-slider', 'value')]
)
def render_payload_scatter_chart(payload_range):
    filtered_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Payload and Launch Success')
    return fig

@app.callback(
    Output('success-bar-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def render_success_bar_chart(selected_site):
    filtered_data = spacex_df[spacex_df['Launch Site'] == selected_site]
    success_counts = filtered_data['class'].value_counts()
    fig = px.bar(x=success_counts.index, y=success_counts.values, title='Launch Success by Site')
    return fig

@app.callback(
    Output('correlation-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def render_correlation_scatter_chart(selected_site):
    filtered_data = spacex_df[spacex_df['Launch Site'] == selected_site]
    fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Launch Success')
    return fig

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
    