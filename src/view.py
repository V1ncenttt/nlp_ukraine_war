import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
from io import BytesIO
import base64
from src.model import Model
from src.wordcloud_hashtags import generateWordcloud

# Loading the database from the 'Model' class
models = {
    '02/04': Model('data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv'),
    '08/04': Model('data/Tweets Ukraine/0408_UkraineCombinedTweetsDeduped.csv'),
    '05/05 to 05/07': Model('data/Tweets Ukraine/0505_to_0507_UkraineCombinedTweetsDeduped.csv'),
    '19/08': Model('data/Tweets Ukraine/0819_UkraineCombinedTweetsDeduped.csv'),
    '31/08': Model('data/Tweets Ukraine/0831_UkraineCombinedTweetsDeduped.csv'),
    '08/09': Model('data/Tweets Ukraine/0908_UkraineCombinedTweetsDeduped.csv'),
    '15/09': Model('data/Tweets Ukraine/0915_UkraineCombinedTweetsDeduped.csv')
    # Ajoutez d'autres modèles si nécessaire
}

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

fig = go.Figure(
    data=go.Choropleth(
        locations=["ITA", "UK", "FRA"],  # replace with your actual locations
        z=[1.0, 2.0, 3.0],  # replace with your actual data
        locationmode="ISO-3",  # or 'country names' for country-level map
        colorscale="Reds",
        autocolorscale=False,
        text=["Arizona", "California", "New York"],  # replace with your actual text
        marker_line_color="white",
        colorbar_title="Colorbar Title Goes Here",
    )
)

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap"
]


class View:
    def __init__(self) -> None:
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self) -> None:
        # Liste des modèles pour le menu déroulant
        model_options = [{'label': model_name, 'value': model_name} for model_name in models.keys()]

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
                    value=list(models.keys())[0],  # Par défaut, sélectionnez le premier modèle
                    style={'width': '50%'}
                ),
                dcc.Dropdown(
                    id='sample-dropdown',
                    options=[
                        {'label': 'WordCloud', 'value': 'wordcloud'},
                    ],
                    value='scatter'
                ),
                #dcc.Graph(id='sample-graph'),
                html.Img(id='wordcloud-image', style={'width': '100%', 'height': 'auto'}),
            ], style=body_style)
        ])

    def setup_callbacks(self):
        @self.app.callback(
            Output('wordcloud-image', 'src'),
            [Input('sample-dropdown', 'value'),
             Input('model-dropdown', 'value')]
        )
        def update_graph(selected_value, selected_model):
            # Charger le modèle sélectionné
            model = models[selected_model]
            df = model.getData().sample(n=1000)  # Exemple: Sélectionnez un échantillon aléatoire de 1,000 tweets

            wordcloud_image = None

            
            if selected_value == 'wordcloud':
                wordcloud_image = self.generate_wordcloud_image(df)
           

            return wordcloud_image

    def generate_wordcloud_hashtags_image(self, df):
        img_binary = generateWordcloud(df)
        img_src = f"data:image/png;base64,{base64.b64encode(img_binary).decode()}"
        return img_src

    def run(self):
        self.app.run_server(debug=True)

