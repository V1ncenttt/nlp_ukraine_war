import dash_core_components as dcc
from src.controller import Controller

class DropdownCreator:
    
    def create_date_dropdown(self, dates):
        return dcc.Dropdown(
            id='date-dropdown',
            options=[{'label': date, 'value': date} for date in dates],
            value='02/04'
        )
    
    def create_choropleth_option_dropdown(self):
        return dcc.Dropdown(
            id='choropleth-option-dropdown',
            options=[{'label': 'Option 1', 'value': 'option1'}, {'label': 'Option 2', 'value': 'option2'}],
            value='option1'
        )
        
    def create_wordcloud_dropdown(self,id):
        return dcc.Dropdown(
            id=id,
            options=[{'label': 'Hashtags Wordcloud', 'value': 'wordcloud1'}, {'label': 'Nouns Wordcloud', 'value': 'wordcloud2'}],
            value='wordcloud1'
        )

    def create_country_dropdown(self, countries):
        return dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in countries],
            value='France'
        )
    
    def create_bar_chart_dropdown(self):
        return dcc.Dropdown(
            id='bar-chart-dropdown',
            options=[{'label': 'Retweets', 'value': 'retweets'}, {'label': 'Likes', 'value': 'likes'}],
            value='likes'
        )
