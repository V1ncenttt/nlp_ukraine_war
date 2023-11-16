import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd


banner_style = {
    'backgroundColor': 'white',
    'padding': '10px',
    'textAlign': 'center',
    'display': 'flex',
    'color': 'black',
    'fontSize': '24px',
    'fontFamily': 'Open Sans, sans-serif',
    'font-weight': '700'
}

body_style = {
    'backgroundColor': '#f8f8f8',  # Light gray background
    'padding': '20px',
    'fontFamily': 'Open Sans, sans-serif'
}

external_stylesheets = ['https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap']

class View:
    def __init__(self) -> None:
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self) -> None:
        self.app.layout = html.Div([
            html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=dash.get_asset_url("ukr_flag.png"), style={'height':'50px', 'border-radius':'10px', 'marginRight': '10px'}),
                     html.Div("Ukrainian War: a global opinion analysis using twitter data", style={'fontSize': '24px', 'padding-top':'10px'}) 
                      ],
            style=banner_style
            ),
            html.Div([
            dcc.Dropdown(
                id='sample-dropdown',
                options=[
                    {'label': 'Scatter Plot', 'value': 'scatter'},
                    {'label': 'Line Plot', 'value': 'line'},
                ],
                value='scatter'
            ),
            dcc.Graph(id='sample-graph')
            ], style=body_style)
        ])

    def setup_callbacks(self):
        @self.app.callback(
            Output('sample-graph', 'figure'),
            Input('sample-dropdown', 'value')
        )
        
        def update_graph(selected_value):
            df = px.data.iris()  # Sample dataset
            if selected_value == 'scatter':
                fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species')
            else:
                fig = px.line(df, x='sepal_width', y='sepal_length', color='species')
            return fig

    def run(self):
        self.app.run_server(debug=True)

