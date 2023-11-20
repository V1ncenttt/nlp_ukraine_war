import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from src.model import Model
from PIL import Image
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Loading the database from the 'Model' class
M=Model('data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv')
df=M.getData()
# Selecting a random sample of 50,000 tweets
df=df.sample(n=100)
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
    
    # Load the Ukrainian flag image as a mask
    mask = Image.open('data/drapeau-ukraine.png').convert('RGBA')
    white_bg = Image.new('RGBA', mask.size, 'WHITE')
    white_bg.paste(mask, (0,0), mask)
    white_bg.convert('RGB')
    ukraine_shape_mask = np.array(white_bg)
    ukraine_coloring=np.array(Image.open('data/drapeau-ukraine.png'))
    # Create the WordCloud with the Ukrainian flag mask and specific colors
    wordcloud = WordCloud(width=800, height=400, background_color='white', mask=ukraine_shape_mask,
                          contour_width=1, contour_color='blue', colormap='YlOrBr').generate(all_hashtags)
    image_colors=ImageColorGenerator(ukraine_coloring)
    # Display the WordCloud using matplotlib
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
    plt.axis('off')
    plt.show()

    
# Generating and displaying the WordCloud
generateWordcloud(df)
