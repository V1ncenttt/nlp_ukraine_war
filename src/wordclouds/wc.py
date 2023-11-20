from wordcloud import WordCloud
from wordcloud import STOPWORDS
from wordcloud import ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as es_stopwords

# Importation du dataframe panda
data = pd.read_csv("../data/0908_UkraineCombinedTweetsDeduped.csv")
data =data.head(1000)

if __name__=="__main__":
    
    # Pour retirer les mots "parasite"
    stopwords = set(STOPWORDS)
    stopwords.add('https')
    stopwords.add('t')
    stopwords.add('co')
    stopwords |= set(es_stopwords)

    text = " ".join(i for i in data['text'])

    colors = ImageColorGenerator(np.array(Image.open('map.png')))

    # Création du WordCloud
    wordcloud = WordCloud(stopwords=stopwords, normalize_plurals=True, max_font_size=40,
                          background_color='white', mask=np.array(Image.open('map.png')), 
                          color_func=colors, contour_color='black', contour_width=2).generate(text)

    # Affichage du WordCloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
