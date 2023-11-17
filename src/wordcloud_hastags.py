import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.model import Model
import nltk

nltk.download('punkt')
nltk.download('stopwords')

#Chargement de la base de donnée à partir de la classe model
M=Model('data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv')
df=M.getData()
#sélection d'un échantillon aléatoire de 50 000 tweets
df=df.sample(n=50000)

def generateWordcloud(df):
    if 'hashtags' not in df.columns:
        raise ValueError("La colonne 'hashtags' n'existe pas dans le DataFrame.")

    # Concaténation de tous les hashtags dans une seule chaîne de caractères
    all_hashtags = ' '.join(df['hashtags'].sum())

    # Création du WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_hashtags)

    # Affichage du WordCloud à l'aide de matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
generateWordcloud(df)
