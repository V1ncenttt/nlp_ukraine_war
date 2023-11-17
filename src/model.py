import pandas as pd
import re
import ast

class Model:
    def __init__(self, dataset) -> None:
        self.data = pd.read_csv(dataset)
        useless=["userid", "tweetid", "following", "totaltweets", "original_tweet_id", "original_tweet_user_id", "original_tweet_username", "in_reply_to_status_id", "in_reply_to_user_id", "in_reply_to_screen_name", "is_quote_status", "quoted_status_id", "quoted_status_userid", "quoted_status_username", "extractedts", "coordinates"]
    #suppression des colonnes inutiles
        for m in useless:
            if m in self.data.columns:
                self.data.drop(m, inplace=True, axis=1)
        self.delete_links()
        self.extract_hashtags()
    def delete_links(self):
    # Utiliser une expression régulière pour rechercher les liens
        regex_liens = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    # Remplacer les liens par une chaîne vide
        self.data['tweet']= self.data["text"].apply(lambda x: re.sub(regex_liens, '', str(x)))
        
    def extract_hashtags(self):
    # Voir si la colonne 'hashtasg' existe dans le DataFrame
        if 'hashtags' not in self.data.columns:
            raise ValueError("La colonne 'hashtags' n'existe pas dans le DataFrame.")
         
    #Convertir les chaînes JSON en listes Python
        self.data['hashtags'] = self.data['hashtags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
        self.data['hashtags'] = self.data['hashtags'].apply(lambda x: [tag['text'] for tag in x] if isinstance(x, list) else [])
        return self.data

    def __str__(self) -> str:
        return str(self.data)

    def getData(self) -> None:
        return self.data
    
if __name__=='__main__':
    M=Model('../data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv')
