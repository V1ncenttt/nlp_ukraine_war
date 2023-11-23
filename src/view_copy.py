import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
from io import BytesIO

from src.controller import Controller
from src.header import Header
from src.visualizor import Visualizor
from src.dropdown_creator import DropdownCreator
# Loading the database from the 'Model' class


body_style = {
    "backgroundColor": "#f8f8f8",  # Light gray background
    "padding": "20px",
    "fontFamily": "Open Sans, sans-serif",
}



external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap"
]

    
class View:
    def __init__(self) -> None:
        self.app = dash.Dash(__name__)
        self.controller = Controller()
        self.setup_layout()
        self.setup_callbacks()

    def run(self):
        self.app.run_server(debug=False)

    def setup_layout(self):
        self.app.layout =  html.Div([
            Header().create_header(), # Header of the website
            html.Div([ # Body
                html.Div([
                    DropdownCreator().create_date_dropdown(self.controller.get_dates()),
                    html.Div([
                        DropdownCreator().create_option_dropdown('map-dropdown'),
                        Visualizor().create_choropleth_map(self.controller.get_choropleth_data('02/04', 'option1'))
                    ]),
                    html.Div([
                        DropdownCreator().create_option_dropdown('bar-chart-dropdown'),
                        Visualizor().create_bar_chart(None)
                    ]),
                    html.Div([
                        DropdownCreator().create_option_dropdown('wordcloud-dropdown'),
                        Visualizor().create_wordcloud(None)
                    ]),
                ]),
                html.Div([
                        DropdownCreator().create_country_dropdown(self.controller.get_all_countries()),
                        Visualizor().create_line_chart(None)
                ])
            ], style=body_style)
        ])
    
    def setup_callbacks(self):
        @self.app.callback(
        Output('choropleth-map', 'figure'),
        [Input('date-dropdown', 'value'), Input('choropleth-option-dropdown', 'value')]
        )
        def update_choropleth(selected_date, selected_option):
            data = self.controller.get_choropleth_data(selected_date, selected_option)
            figure = Visualizor().create_choropleth(data)  
            return figure

        @self.app.callback(
        Output('bar-chart', 'figure'),
        [Input('date-dropdown', 'value'), Input('bar-chart-dropdown', 'value')]
        )
        def update_bar_chart(selected_date, selected_option):
            data = None
            figure = Visualizor().create_bar_chart(data)
            return figure
    

        @self.app.callback(
        Output('wordcloud', 'figure'),
        [Input('date-dropdown', 'value'), Input('wordcloud-dropdown', 'value')]
        )
        def update_wordcloud(selected_date, selected_option):
            data = None
            figure = Visualizor().create_wordcloud(data)
            return figure
        
        @self.app.callback(
        Output('line-chart', 'figure'),
        [Input('country-dropdown', 'value')]
        )
        def update_line_chart(selected_country):
            data = None
            figure = Visualizor().create_line_chart(data)
            return figure


if __name__ == "__main__":
    view = View()
    view.run()