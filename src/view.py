import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd

class View:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        self.app.layout = html.Div([
            dcc.Dropdown(
                id='sample-dropdown',
                options=[
                    {'label': 'Scatter Plot', 'value': 'scatter'},
                    {'label': 'Line Plot', 'value': 'line'},
                ],
                value='scatter'
            ),
            dcc.Graph(id='sample-graph')
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

