from src.model import Model
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.model import Model
from PIL import Image
from io import BytesIO
import numpy as np
import nltk




class Controller:
    """
    The Controller class that manages multiple models.

    This class holds a dictionary of models, each associated with a specific date. 
    It provides methods to interact with these models.

    Attributes:
        models (dict): A dictionary where the keys are dates and the values are instances of the Model class,
        corresponding to a dataset.
    """

    def __init__(self):
        self.models = {
            "04/02": Model("data/tweets_processed/0402_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "04/08": Model("data/tweets_processed/0408_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "05/05 to 05/07": Model("data/tweets_processed/0505_to_0507_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "08/19": Model("data/tweets_processed/0819_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "08/31": Model("data/tweets_processed/0831_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "09/08": Model("data/tweets_processed/0908_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "09/15": Model("data/tweets_processed/0915_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            }

    def do_something(self):
        # Call a method from the model
        self.model.some_method()


if __name__ == "__main__":
    controller = Controller()
