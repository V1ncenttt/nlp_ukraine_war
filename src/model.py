import pandas as pd
from textblob import TextBlob
from geopy.geocoders import OpenCage
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import re
import ast

class Model:
    def __init__(self, dataset : pd.DataFrame) -> None:
        self.data = pd.read_csv(dataset)
        useless=["userid", "tweetid", "following", "totaltweets", "original_tweet_id", "original_tweet_user_id", "original_tweet_username", "in_reply_to_status_id", "in_reply_to_user_id", "in_reply_to_screen_name", "is_quote_status", "quoted_status_id", "quoted_status_userid", "quoted_status_username", "extractedts", "coordinates"]
    #removing unnecessary columns
        for m in useless:
            if m in self.data.columns:
                self.data.drop(m, inplace=True, axis=1)
        
        self.add_sadness()
        self.delete_links()
        self.extract_hashtags()
        

    def sad(self, tweet: str):
        blob=TextBlob(tweet)
        return blob.sentiment.polarity<0 
    
    def add_sadness(self):
        self.data["sadness"]=self.data["text"].apply(lambda x: self.sad(x))
        
    def sort_by_favourite(self):
        """
        Sorts the DataFrame based on the 'favorite_count' column in descending order.

        This method first converts the 'favorite_count' column to integer type.
        Then, it sorts the DataFrame stored in the 'data' attribute based on the 'favorite_count' column in descending order.
        The sorted DataFrame is printed to the console.

        Additionally, it extracts the usernames of the top 15 users with the most favorite tweets and prints the list.

        Returns:
            None
        """
    # Convert 'favorite_count' column to integer
        self.data['favorite_count'] = self.data['favorite_count'].astype(int)

    # Sort DataFrame based on 'favorite_count' in descending order
        df_sorted = self.data.sort_values(by='favorite_count', ascending=False)
        print(df_sorted)

    # Extract the usernames of the top 15 users with the most favorite tweets
        list_sorted_id = df_sorted['username'].tolist()[:15]
        print("List sorted IDs by favorite tweets:", list_sorted_id)

    
    def sort_retweets(self):
        """
            Sorts the DataFrame based on the 'retweetcount' column in descending order and prints the sorted DataFrame.

            This method sorts the DataFrame stored in the 'data' attribute based on the 'retweetcount' column in descending order.
            The sorted DataFrame is then printed to the console.

            Additionally, it extracts the usernames of the top 20 users with the most retweets and prints the list.

            Returns:
                 None
        """
         
        df_sort = self.data.sort_values(by = "retweetcount", ascending=False)
        print(df_sort)
    # Extract the usernames of the top 20 users with the most retweets
        list_sorted_name = df_sort['username'].tolist()[:20]
        print("List of users with the most retweets:", list_sorted_name)
    
    def delete_links(self):
            """
            Removes hyperlinks from the 'text' column in the DataFrame.

            This method uses a regular expression to find hyperlinks in the 'text' column of the DataFrame.
            It then replaces these hyperlinks with an empty string, modifying the 'tweet' column in place.

            Returns:
                None
            """
    #Use a regular expression to find links
            regex_liens = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    #Replace links with empty string
            self.data['tweet']= self.data["text"].apply(lambda x: re.sub(regex_liens, '', str(x)))
        
    def extract_hashtags(self):
        """
        Extracts hashtags from the 'hashtags' column in the DataFrame.

        This method checks if the 'hashtags' column exists in the DataFrame.
        If it doesn't, a ValueError is raised.

        It then converts the JSON strings in the 'hashtags' column to Python lists,
        and further processes the lists to extract the 'text' field of each hashtag.
        The extracted hashtags are stored in a new 'hashtags' column in the DataFrame.

        Returns:
            pandas.DataFrame: The DataFrame with the extracted hashtags in the 'hashtags' column.
        Raises:
            ValueError: If the 'hashtags' column is not present in the DataFrame.
        """
    #See if the 'hashtags' column exists in the DataFrame
        if 'hashtags' not in self.data.columns:
            raise ValueError("La colonne 'hashtags' n'existe pas dans le DataFrame.")
         
    #Convert JSON strings to Python lists
        self.data['hashtags'] = self.data['hashtags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
        self.data['hashtags'] = self.data['hashtags'].apply(lambda x: [tag['text'] for tag in x] if isinstance(x, list) else [])
        return self.data

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        This method is invoked when the `str()` function is called on an instance of the class.
        It returns a string representation of the 'data' attribute, which is the main DataFrame.

        Returns:
            str: A string representation of the DataFrame stored in the 'data' attribute.
        """
        return str(self.data)


 
      

###    def find_country(self, city: str)-> str:
        """
        Finds the country associated with a given city using geocoding.

        Args:
             - city (str): The name of the city for which the country needs to be found.

         Returns:
             - str: The country name if the city is found; an empty string if the city is invalid or not provided;
                a space character if the location is an empty string;
                "Emplacement non trouvé" if the location is not found;
             An error message if an exception occurs during the geocoding process.
        """
    # A cache dictionary to store previously found city-country mappings for efficiency
        cache={}
        
    # Check if the city is already in the cache and return the country if found
 
        if city in cache:
            return cache[city]
        
    # Check if the provided city is invalid, empty, or not a string
        
        if pd.isnull(city) or (not isinstance(city, str)) or (not city.strip()):
            return ""
            
    # Initialize a geolocator with a user agent for geocoding

        geolocator = Nominatim(user_agent="mon_application")

        try:
            # Attempt to geocode the provided city
            location = geolocator.geocode(city)
            # If a location is found, extract the country and update the cache
            if location:
                country = location.address.split(",")[-1].strip()
                cache[city]=country
                return country
            # If the location is an empty string, return a space character
            if location=='':
                return " "
            else:
            # If the location is not found, return a specific message
                return "Emplacement non trouvé"
            
        except Exception as e:
            # If an exception occurs during the geocoding process, return an error message
            return f"Une erreur s'est produite : {str(e)}"
    
    def apply_find_country(self) -> pd.DataFrame:
        """applies the find_country function to the entire location column

        Returns:
            pd.DataFrame: the modified location column
        """
        self.data['location']=self.data.head(5)['location'].apply(lambda x: self.find_country(x))
        return self.data
    
    def getData(self) -> pd.DataFrame:
        return self.data
    
if __name__=='__main__':
    M=Model('../data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv')
    M.apply_find_country()
    print(M.data['location'])
    M.sort_retweets()
    