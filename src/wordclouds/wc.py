from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from PIL import Image
import numpy as np
import pandas as pd
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as es_stopwords

# Panda dataframe importation
data = pd.read_csv("../../data/0908_UkraineCombinedTweetsDeduped.csv")

if __name__ == "__main__":
    # Creating stopwords list
    stopwords = set(STOPWORDS)
    stopwords.add("https")
    stopwords.add("t")
    stopwords.add("co")
    stopwords.add("will")
    stopwords |= set(es_stopwords)  # Stopwords espagnols

    # Creating a string containing all the tweets
    text = " ".join(i for i in data["text"])

    # Load the Ukrainian flag image as a mask
    mask = Image.open('drapeau-ukraine.png').convert('RGBA')
    white_bg = Image.new('RGBA', mask.size, 'WHITE')
    white_bg.paste(mask, (0,0), mask)
    white_bg.convert('RGB')
    ukraine_shape_mask = np.array(white_bg)

    # Colors of the wordcloud
    custom_colors = ['royalblue', 'gold']
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

    # Displaying wordcloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
