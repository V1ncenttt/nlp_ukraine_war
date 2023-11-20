import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.model import Model
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Loading the database from the 'Model' class
M=Model('data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv')
df=M.getData()
# Selecting a random sample of 50,000 tweets
df=df.sample(n=50)
#df=df.head(4)
def generateWordcloud(df):
    """
    Generates and displays a WordCloud based on hashtags in the DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing tweet data.

    Raises:
        ValueError: If the 'hashtags' column is not present in the DataFrame.
    """
    
# Check if the 'hashtags' column exists in the DataFrame
    if 'hashtags' not in df.columns:
        raise ValueError("La colonne 'hashtags' n'existe pas dans le DataFrame.")

# Concatenate all hashtags into a single string
    all_hashtags = ' '.join(df['hashtags'].sum())

# Create the WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_hashtags)

# Display the WordCloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    
# Generating and displaying the WordCloud
generateWordcloud(df)
