import pandas as pd
from geopy.geocoders import OpenCage
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from concurrent.futures import ThreadPoolExecutor

class Country:
    def __init__(self, dataset : pd.DataFrame) -> None:
        self.data = pd.read_csv(dataset)
    
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
        """applies the find_country function to the entire location column

        Returns:
            pd.DataFrame: the modified location column
        """
        self.data['location']=self.data.head(5)['location'].apply(lambda x: self.find_country(x))
        return self.data
    
    def apply_fin_country2(self) -> pd.DataFrame:
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

if __name__=='__main__':
    C = Country('../data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv')
    C.apply_fin_country2()