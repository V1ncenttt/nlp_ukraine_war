import pandas as pd
import numpy as np
import re
import os
import pycountry
import geonamescache
import swifter
from functools import lru_cache

class DataPreproccessing:
    def __init__(self, dataset: pd.DataFrame) -> None:
        self.data = pd.read_csv(dataset, low_memory=False)
        
        self.route = dataset
        self.cache = {'New York': 'USA', 'England': 'GBR', 'NYC': 'USA', 'Boston':'USA'}
        self.data['location'] = self.data['location'].astype(str)
        self.gc = geonamescache.GeonamesCache()
        self.countries = self.gc.get_countries()
        self.pc = pycountry.countries
            
    @lru_cache(maxsize=None)
    def geocode(self, location: str):
        
        if location == 'nan' or len(location.split(' ')) >3:
            return None
        
        loc = location.split(',')[0].strip()

        if location in self.cache: 
            return self.cache[location]
        if loc in self.cache:
            return self.cache[loc]
        
        loc2 = location.split(',')[-1].strip()

        country = self.geocode_helper(loc)

        if country is None:
            country = self.geocode_helper(loc2)

        if country is None:
            try:
                country = self.pc.search_fuzzy(loc2)[0].alpha_3
            except LookupError:
                self.cache[location] = None
                return None
            
        self.cache[location] = country
        self.cache[loc] = country
        return country
        
        
    def geocode_helper(self, location: str):
        try:
            country = self.countries[location]['iso']
            return country
        
        except KeyError:
            
            try:
                countries = self.gc.get_cities_by_name(location)
                key =list(countries[0].keys())[0]
                country = countries[0][key]['countrycode']
                return country
            except LookupError as e:
                return None
            except IndexError as e:
                return None

    def apply_geocode(self):
        self.data["country"] = self.data["location"].swifter.apply(lambda x: self.geocode(x))

    @lru_cache(maxsize=None)
    def country_iso(self, country: str):
        # List of all the countries found (some are None)
        if country == 'xk':
            return 'XKX'
        if country == 'nan' or country == None:
            return None
        try:
            nation = pycountry.countries.search_fuzzy(country)[0]
            return nation.alpha_3
        except LookupError:
            # Handle the case where the country name is not found
            return None
        
    
    def apply_iso(self):
        self.data["ISO"] = self.data["country"].swifter.apply(lambda x: self.country_iso(x))

    def delete_links(self):
        """
        Removes hyperlinks from the 'text' column in the DataFrame.

        This method uses a regular expression to find hyperlinks in the 'text' column of the DataFrame.
        It then replaces these hyperlinks with an empty string, modifying the 'tweet' column in place.

        Returns:
            None
        """
        # Use a regular expression to find links
        regex_liens = re.compile(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        )
        # Replace links with empty string
        self.data["tweet"] = self.data["text"].apply(
            lambda x: re.sub(regex_liens, "", str(x))
        )

    def unnecessary_columns(self):
        useless = [
            "userid",
            "tweetid",
            "following",
            "totaltweets",
            "original_tweet_id",
            "original_tweet_user_id",
            "original_tweet_username",
            "in_reply_to_status_id",
            "in_reply_to_user_id",
            "in_reply_to_screen_name",
            "is_quote_status",
            "quoted_status_id",
            "quoted_status_userid",
            "quoted_status_username",
            "extractedts",
            "coordinates",
        ]
        # removing unnecessary columns
        for m in useless:
            if m in self.data.columns:
                self.data.drop(m, inplace=True, axis=1)

    def back_to_csv(self):
        self.data.to_csv(
            "../data/tweets_processed/" + os.path.basename(self.route).replace(".csv", "") + "_PROCESSED.csv"
        )

    def preprocess_data(self):
        print('starting preprocessing for {}...'.format(os.path.basename(self.route)))
        self.unnecessary_columns()
        print('done removing unnecessary columns')
        self.delete_links()
        print('done deleting links')
        self.apply_geocode()
        print('done geocoding')
        self.apply_iso()
        print('done applying iso')
        self.back_to_csv()
        print('done preprocessing for {}'.format(os.path.basename(self.route)))
        print('-----------------------------------')


if __name__ == "__main__":
    Data = [
        #"../data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0408_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0505_to_0507_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0819_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0831_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0908_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0915_UkraineCombinedTweetsDeduped.csv",
    ]
    for fichier in Data:
        D = DataPreproccessing(fichier)
        
        D.preprocess_data()
        print('Done creating all of the preprocessed files')
