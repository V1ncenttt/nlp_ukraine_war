import pandas as pd
from textblob import TextBlob



class Model:
    def __init__(self, dataset):
        self.data = pd.read_csv(dataset)
        useless=["userid", "tweetid", "following", "totaltweets", "original_tweet_id", "original_tweet_user_id", "original_tweet_username", "in_reply_to_status_id", "in_reply_to_user_id", "in_reply_to_screen_name", "is_quote_status", "quoted_status_id", "quoted_status_userid", "quoted_status_username", "extractedts", "coordinates"]
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
        list_sorted_id = df_sorted['username'].tolist()[:10]   
        print("List sorted IDs by favourite tweets:", list_sorted_id)
    
if __name__=='__main__':
    M=Model('../data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv')
    M.sortByFavourite()
    