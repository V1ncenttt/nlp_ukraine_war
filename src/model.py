import pandas as pd
from textblob import TextBlob
from geopy.geocoders import OpenCage
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim


import re

class Model:
    def __init__(self, dataset) -> None:
        self.data = pd.read_csv(dataset)
        useless=["userid", "tweetid", "following", "totaltweets", "original_tweet_id", "original_tweet_user_id", "original_tweet_username", "in_reply_to_status_id", "in_reply_to_user_id", "in_reply_to_screen_name", "is_quote_status", "quoted_status_id", "quoted_status_userid", "quoted_status_username", "extractedts", "coordinates"]
    #suppression des colonnes inutiles
        for m in useless:
            if m in self.data.columns:
                self.data.drop(m, inplace=True, axis=1)
        self.addSadness()
        
 
        
    def sad(self, tweet):
        blob=TextBlob(tweet)
        return blob.sentiment.polarity<0 
    
    def addSadness(self):
        self.data["sadness"]=self.data["text"].apply(lambda x: self.sad(x))

# trier par tweets plus connues
# creer une liste des personnes avec les tweets les plus connues
    def sortByFavourite(self):
        self.data['favorite_count'] = self.data['favorite_count'].astype(int)
        df_sorted = self.data.sort_values(by='favorite_count', ascending=False)
        print(df_sorted)
        list_sorted_id = df_sorted['username'].tolist()[:15]   
        print("List sorted IDs by favourite tweets:", list_sorted_id)
    
        self.delete_links()
        
    def delete_links(self):
    # Utiliser une expression régulière pour rechercher les liens
        regex_liens = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    # Remplacer les liens par une chaîne vide
        self.data['tweet']= self.data["text"].apply(lambda x: re.sub(regex_liens, '', str(x)))
        print(self.data['tweet'][11])

  
      

    def find_country(self, city):
        cache={}
        
        if city in cache:
            return cache[city]
            
        if pd.isnull(city) or (not isinstance(city, str)) or (not city.strip()):
            return ""
        
        geolocator = Nominatim(user_agent="mon_application")

        try:
            location = geolocator.geocode(city)
            if location:
                country = location.address.split(",")[-1].strip()
                cache[city]=country
                return country
            if location=='':
                return " "
            else:
                return "Emplacement non trouvé"
            
        except Exception as e:
            return f"Une erreur s'est produite : {str(e)}"
    
    def apply_find_country(self):
        self.data['location']=self.data.head(5)['location'].apply(lambda x: self.find_country(x))
        return self.data
    
    def getData(self) -> None:
        return self.data
    
if __name__=='__main__':
    M=Model('../data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv')
    M.apply_find_country()
    print(M.data['location'])