from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from PIL import Image
import numpy as np
import pandas as pd
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as es_stopwords

# Importation du dataframe panda
data = pd.read_csv("../../data/0908_UkraineCombinedTweetsDeduped.csv")

if __name__ == "__main__":
    # Pour retirer les mots "parasite"
    stopwords = set(STOPWORDS)
    stopwords.add("https")
    stopwords.add("t")
    stopwords.add("co")
    stopwords.add("will")
    stopwords |= set(es_stopwords)  # Stopwords espagnols

    # Creation d'une chaine de caractere contenant tous les tweets
    text = " ".join(i for i in data["text"])

    # Couleurs du wordcloud
    custom_colors = ["royalblue", "gold"]
    custom_cmap = ListedColormap(custom_colors)

    # Création du wordcloud
    wordcloud = WordCloud(
        stopwords=stopwords,
        height=600,
        width=800,
        normalize_plurals=True,
        colormap=custom_cmap,
        background_color="white",
    ).generate(text)

    # Affichage du wordcloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
