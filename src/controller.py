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
            "02/04": Model("data/tweets_processed/0402_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "08/04": Model("data/tweets_processed/0408_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "05/05 to 07/05": Model("data/tweets_processed/0505_to_0507_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "19/08": Model("data/tweets_processed/0819_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "31/08": Model("data/tweets_processed/0831_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "08/09": Model("data/tweets_processed/0908_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            "15/09": Model("data/tweets_processed/0915_UkraineCombinedTweetsDeduped_PROCESSED.csv"),
            }
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
        df=self.models[date]
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

        return img_binary

    def do_something(self):
        # Call a method from the model
        self.model.some_method()


if __name__ == "__main__":
    controller = Controller()
