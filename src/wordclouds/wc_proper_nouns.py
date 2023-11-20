from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from PIL import Image
import numpy as np
import pandas as pd
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as es_stopwords

# Chargement du modèle spacy en anglais (traitement de langage)
nlp = spacy.load("en_core_web_sm")

# Importation du dataframe panda
data = pd.read_csv("../../data/0908_UkraineCombinedTweetsDeduped.csv").head(1000)


# Fonction pour extraire les noms propres du texte
def nomsPropres(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ == "PERSON"]


if __name__ == "__main__":
    # Pour retirer les mots "parasite"
    stopwords = set(STOPWORDS)
    stopwords.add("https")
    stopwords.add("t")
    stopwords.add("co")
    stopwords |= set(es_stopwords)

    # Extraction des noms propres des tweets
    proper_nouns = [name for text in data["text"] for name in nomsPropres(text)]

    # Couleurs du wordcloud
    custom_colors = ["royalblue", "gold"]
    custom_cmap = ListedColormap(custom_colors)

    # Création du WordCloud
    wordcloud = WordCloud(
        stopwords=stopwords,
        width=800,
        height=400,
        background_color="white",
        colormap=custom_cmap,
    ).generate(" ".join(proper_nouns))

    # show
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
