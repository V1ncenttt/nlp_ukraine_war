import pandas as pd
from geopy.geocoders import OpenCage
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from concurrent.futures import ThreadPoolExecutor
import re
import os


class DataPreproccessing:
    def __init__(self, dataset : pd.DataFrame) -> None:
        self.data = pd.read_csv(dataset)
        self.route = dataset
    
    def find_country(self, city: str)-> str:
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
        # List of addresses you want to geocode
        locations = list(self.data["location"])

        # Number of parallel threads to use (if not specified in ThreadPoolExecutror uses nb cpu times 5)
        num_threads = 10

        with ThreadPoolExecutor() as executor:
            # Use list comprehension to submit geocoding tasks to the executor
            futures = [executor.submit(self.find_country, location) for location in locations]

            # Wait for all tasks to complete and retrieve the results
            countries = [future.result() for future in futures]
            
        #Replaces location of tweets by the countries they are associated to
        self.data["location"] = countries
        return self.data
    
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
        
        return self.data

    def unnecessary_columns(self):
        useless=["userid", "tweetid", "following", "totaltweets", "original_tweet_id", "original_tweet_user_id", "original_tweet_username", "in_reply_to_status_id", "in_reply_to_user_id", "in_reply_to_screen_name", "is_quote_status", "quoted_status_id", "quoted_status_userid", "quoted_status_username", "extractedts", "coordinates"]
        #removing unnecessary columns
        for m in useless:
            if m in self.data.columns:
                self.data.drop(m, inplace=True, axis=1)
        return self.data
    
    def back_to_csv(self):
        self.data.to_csv(os.path.join(self.route, f"{os.path.basename(self.route)}_PROCESS"))



if __name__=='__main__':
    C = DataPreproccessing('../data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv')
    C.unnecessary_columns()
    C.delete_links()
    C.apply_find_country()
    C.back_to_csv()