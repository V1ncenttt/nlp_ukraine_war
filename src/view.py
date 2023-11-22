import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
from io import BytesIO
from src.model import Model
from src.controller import Controller

# Loading the database from the 'Model' class


banner_style = {
    "backgroundColor": "white",
    "padding": "10px",
    "textAlign": "center",
    "display": "flex",
    "color": "black",
    "fontSize": "24px",
    "fontFamily": "Open Sans, sans-serif",
    "font-weight": "700",
}

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
        self.controller = Controller()
        self.app = DashView(self.controller)

    
    def run(self):
        self.app.run()
    
class DashView:
    def __init__(self, controller) -> None:
  
        self.app = dash.Dash(__name__)
        self.controller = controller
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self) -> None:
        # Liste des modèles pour le menu déroulant
        model_options = [{'label': model_name, 'value': model_name} for model_name in self.controller.get_dates()]

        self.app.layout = html.Div([
            html.Div(
                id="banner",
                className="banner",
                children=[
                    html.Img(src=dash.get_asset_url("ukr_flag.png"),
                             style={'height': '50px', 'border-radius': '10px', 'marginRight': '10px'}),
                    html.Div("Ukrainian War: a global opinion analysis using twitter data",
                             style={'fontSize': '24px', 'padding-top': '10px'})
                ],
                style=banner_style
            ),
            html.Div([
                dcc.Dropdown(
                    id='model-dropdown',
                    options=model_options,
                    value=self.controller.get_dates()[0],  # Par défaut, sélectionnez le premier modèle
                    style={'width': '50%'}
                ),
                dcc.Dropdown(
                    id='sample-dropdown',
                    options=[
                        {'label': 'WordCloud', 'value': 'wordcloud'},
                    ],
                    value='scatter'
                ),
                html.Img(id='wordcloud-image', style={'width': '100%', 'height': 'auto'}),
            ], style=body_style),
            dcc.Graph(id='choropleth', figure=self.create_cloropleth(self.controller.get_dates()[0]))
        ])
    def create_cloropleth(self,date):
        loc, position, countries = self.controller.get_polarity_cloropleth_data(date)
        fig = go.Figure(
        data=go.Choropleth(
            locations=loc,  
            z=position,  
            locationmode="ISO-3", 
            colorscale="Reds",
            autocolorscale=False,
            text=[f"{country}: {value}" for country, value in zip(countries, position)], 
            marker_line_color="white",
            colorbar_title="Number of pro-russian tweets",
            )
        )
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},  # Reduce margins to use more space
            geo=dict(
                projection_scale=5,  # Adjust scale of the map
                center=dict(lat=0, lon=0),  # Adjust center
            )
        )
        
        return fig

    def setup_callbacks(self):
        @self.app.callback(
            Output('wordcloud-image', 'src'),
            [Input('sample-dropdown', 'value'),
             Input('model-dropdown', 'value')]
        )
        def update_graph(selected_value, date):
            # Charger le modèle sélectionné

            wordcloud_image = None

            
            if selected_value == 'wordcloud':
                wordcloud_image = self.controller.generate_wordcloud(date)
           

            return wordcloud_image


    def run(self):
        self.app.run_server(debug=False)

