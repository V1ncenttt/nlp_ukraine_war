from src.model import Model
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from PIL import Image
from io import BytesIO
import numpy as np
import nltk
import base64
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as es_stopwords
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px



class Controller:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls)
            # Initialize any attributes of the instance here if needed
        return cls._instance

    def __init__(self):
        # Initialization should only occur if the instance hasn't been initialized before
        self.models = {
        "02/04": Model("data/tweets_processed/0402_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
        "08/04": Model("data/tweets_processed/0408_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
        "05/05 to 07/05": Model("data/tweets_processed/0505_to_0507_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
        "19/08": Model("data/tweets_processed/0819_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
        "31/08": Model("data/tweets_processed/0831_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
        "08/09": Model("data/tweets_processed/0908_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
        "15/09": Model("data/tweets_processed/0915_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
        }

    def get_dates(self) -> list:
        """ 
        Returns a list of dates corresponding to the models."""
        return list(self.models.keys())


    def generate_wordcloud(self, date):
        """
        Generates a WordCloud based on hashtags in the DataFrame.

        Args:
                df (pandas.DataFrame): The DataFrame containing tweet data.

        Returns:
                bytes: The binary data of the PNG image.
        Raises:
                ValueError: If the 'hashtags' column is not present in the DataFrame.
        """
        df=self.models[date].data
        # Check if the 'hashtags' column exists in the DataFrame
        if "hashtags" not in df.columns:
            raise ValueError("La colonne 'hashtags' n'existe pas dans le DataFrame.")

        # Concatenate all hashtags into a single string
        all_hashtags = " ".join(df["hashtags"].sum())

        # Load the Ukrainian flag image as a mask
        mask = Image.open("src/wordclouds/drapeau-ukraine.png").convert("RGBA")
        white_bg = Image.new("RGBA", mask.size, "WHITE")
        white_bg.paste(mask, (0, 0), mask)
        white_bg.convert("RGB")
        ukraine_shape_mask = np.array(white_bg)
        ukraine_coloring = np.array(Image.open("src/wordclouds/drapeau-ukraine.png"))

        # Create the WordCloud with the Ukrainian flag mask and specific colors
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white",
            mask=ukraine_shape_mask,
            contour_width=1,
            contour_color="blue",
            colormap="YlOrBr",
        ).generate(all_hashtags)

        image_colors = ImageColorGenerator(ukraine_coloring)

        # Create a BytesIO buffer to save the WordCloud image
        img_buffer = BytesIO()

        # Save the WordCloud image to the buffer in PNG format
        wordcloud.recolor(color_func=image_colors).to_image().save(img_buffer, format="PNG")

        # Get the binary data of the PNG image
        img_binary = img_buffer.getvalue()
        img_src = f"data:image/png;base64,{base64.b64encode(img_binary).decode()}"
        return img_src
    
    def generate_classical_wordcloud(self,date):
        '''
        Generates a wordcloud considering all the words of the tweets from the dataframe
        corresponding to the date in argument
        
        Returns :
            A png format wordcloud
        '''
        df = self.models[date].data
        # Creating stopwords list
        stopwords = set(STOPWORDS)
        stopwords.add("https")
        stopwords.add("t")
        stopwords.add("co")
        stopwords.add("will")
        stopwords |= set(es_stopwords)  # Stopwords espagnols

        # Creating a string containing all the tweets
        text = " ".join(i for i in df["text"])

        # Loading the Ukrainian flag image as a mask
        mask = Image.open("src/wordclouds/drapeau-ukraine.png").convert("RGBA")
        white_bg = Image.new("RGBA", mask.size, "WHITE")
        white_bg.paste(mask, (0, 0), mask)
        white_bg.convert("RGB")
        ukraine_shape_mask = np.array(white_bg)

        # Colors of the wordcloud
        custom_colors = ["royalblue", "gold"]
        custom_cmap = ListedColormap(custom_colors)

        # Creating wordcloud
        wordcloud = WordCloud(
            stopwords=stopwords,
            height=400,
            width=800,
            mask=ukraine_shape_mask,
            normalize_plurals=True,
            colormap=custom_cmap,
            background_color="white",
        ).generate(text)

        # Creating a BytesIO buffer to save the WordCloud image
        img_buffer = BytesIO()

        # Saving the WordCloud image to the buffer in PNG format
        wordcloud.to_image().save(img_buffer, format="PNG")

        # Getting the binary data of the PNG image
        img_binary = img_buffer.getvalue()
        img_src = f"data:image/png;base64,{base64.b64encode(img_binary).decode()}"
        return img_src


    def get_polarity_cloropleth_data(self, date):
        """
        Generates a DataFrame containing the polarity of each country.

        Args:
                date (str): The date of the model to use.

        Returns:
                pandas.DataFrame: The DataFrame containing the polarity of each country.
        """
        df=self.models[date].data
        # Group by country and get the mean polarity of each country
        print(df[df['conflict_position'] == 1])
        polarity_df = df.groupby(['ISO', 'country'])['conflict_position'].apply(lambda x: (x == 1).sum()).reset_index() 
        # Remove countries with no polarity
        polarity_df = polarity_df[polarity_df["conflict_position"].notna()]

        iso_list = polarity_df['ISO'].tolist()
        polarity_list = polarity_df['conflict_position'].tolist()
        countries_list = polarity_df['country'].tolist()
        print(iso_list, polarity_list, countries_list)
        return iso_list, polarity_list, countries_list

    def polarity_over_time(self, country:str):
        # Getting the average polarity for each day (so each dataframe)
        average_polarities = []
        dates = ['02/04','08/04','05/05','19/08','31/08','08/09','15/09']
        for model in self.models:
            average_polarities.append(model.get_average_polarity_for_country(country))
        
        # Displaying the graph
        plt.plot(dates,average_polarities)
        plt.xlabel('Date')
        plt.ylabel('Average polarity of the tweets from the country')
        plt.show()
        
    def favourite_users(self, date):
        model=self.models[date]
        return model.sort_by_favourite()
    
    