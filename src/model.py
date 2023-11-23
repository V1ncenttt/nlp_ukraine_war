import pandas as pd
from textblob import TextBlob
import torch
import ast
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset


class Model:

    """
    The Model class that handles the processing and analysis of the dataset.

    This class reads a CSV file into a DataFrame, samples a subset of the data, and drops unnecessary columns.
    It provides methods to perform sentiment analysis, geolocation, and other data processing tasks.

    Attributes:
        data (pd.DataFrame): The DataFrame holding the dataset.
    """

    def __init__(self, dataset: pd.DataFrame) -> None:
        print("Loading dataset...")
        self.data = pd.read_csv(dataset, engine='python')
        self.data = self.data.sample(n=10)
        self.data['text'] = self.data['text'].astype(str)
        self.loadModel()
        self.add_polarity()
        self.add_sadness()
        self.extract_hashtags()
        print("Done!")

    def polarity(self, tweet: str):
        """
        Calculate the polarity of a given text.

        This method uses a sentiment analysis model to calculate the polarity of the input text.
        The polarity is a float between -1.0 and 1.0, where -1.0 means very negative sentiment, 0 means neutral sentiment, and 1.0 means very positive sentiment.

        Parameters:
        text (str): The text to analyze.

        Returns:
        float: The polarity of the text.
        """
        if tweet == None:
            return 0
        blob = TextBlob(tweet)
        return blob.sentiment.polarity

    def get_average_polarity_for_country(self, country: str) -> float:
        """
        Calculate the average polarity per country.

        This method uses the 'polarity' and 'country' attributes of the tweets in the dataset.
        It calculates the average polarity for each country and returns a dictionary where the keys are country names and the values are the average polarity.

        Returns:
        float: float mapping country names to average polarity.
        """
        return self.data[self.data["location"] == country]["polarity"].mean()

    def add_polarity(self) -> None:
        """
        Add a 'polarity' column to the dataset.

        This method applies the 'polarity' method to the 'text' column of the dataset, and stores the result in a new 'polarity' column.
        The 'polarity' column will contain the polarity of each tweet.
        """
        self.data["polarity"] = self.data["text"].apply(lambda x: self.polarity(x))

    def add_sadness(self) -> None:
        self.data["sadness"] = self.data["text"].apply(lambda x: self.polarity(x) < 0)

    def sort_by_favorite(self):
        """
        Sorts the DataFrame based on the 'favorite_count' column in descending order.

        This method first converts the 'favorite_count' column to integer type.
        Then, it sorts the DataFrame stored in the 'data' attribute based on the 'favorite_count' column in descending order.
        The sorted DataFrame is printed to the console.

        Additionally, it extracts the usernames and favorite counts of the top 15 users with the most favorite tweets
        and prints the list and a dictionary with usernames as keys and favorite counts as values.
        Returns:
            None
        """
        
        # Convert 'favorite_count' column to integer
        self.data["favorite_count"] = self.data["favorite_count"].astype(int)

        # Sort DataFrame based on 'favorite_count' in descending order
        df_sorted = self.data.sort_values(by="favorite_count", ascending=False)
        print(df_sorted)

        # Extract the usernames and favorite counts of the top 15 users with the most favorite tweets
        top_users = df_sorted[["username", "favorite_count"]].head(15)

        # Print list of sorted IDs by favorite tweets
        list_sorted_id = top_users["username"].tolist()
        print("List sorted IDs by favorite tweets:", list_sorted_id)

        # Convert the top_users DataFrame to a dictionary
        user_likes_dict = top_users.set_index("username")["favorite_count"].to_dict()

        # Print the dictionary
        print("Dictionary of usernames and favorite counts:", user_likes_dict)

    def sort_retweets(self):
        """
        Sorts the DataFrame based on the 'retweetcount' column in descending order and prints the sorted DataFrame.

        This method sorts the DataFrame stored in the 'data' attribute based on the 'retweetcount' column in descending order.
        The sorted DataFrame is then printed to the console.

        Additionally, it extracts the usernames of the top 20 users with the most retweets and prints the list.

        Returns:
             None
        """

        df_sort = self.data.sort_values(by="retweetcount", ascending=False)
        print(df_sort)
        # Extract the usernames of the top 20 users with the most retweets
        list_sorted_name = df_sort["username"].tolist()[:20]
        print("List of users with the most retweets:", list_sorted_name)

    def most_active_countries(self):
        """
        This function returns a list of the 10 most active countries
        of the studied DataFrame.

        This function will be usefull if we add functionalities to our App that could potentially happen in a future update of our MVP.
        """
        # List of each country's number of tweets

        count_countries = self.data["Country"].value_counts()

        # Takes the 10 highest values
        mostActiveCountries = count_countries.head(10).index.tolist()
        print("List of the most active countries :", mostActiveCountries)

    def most_active_user(self):
        """
        This function returns a list of the 20 most active users ('username' column)
        of the studied DataFrame.

        It counts each user's number of tweets and takes the 20 highest values in a list.

        Returns :
            String : "List of the most active users :" and the list.

        This function will be usefull if we add functionalities to our App that could potentially happen in a future update of our MVP.
        """
        # List of each user's number of tweets
        counts = self.data["username"].value_counts()

        # Takes the 20 highest values
        active_users = counts.head(20).index.tolist()
        print("List of the most active users :", active_users)

    def most_oriented_countries(self):
        """
        From a DataFrame, containing the columns 'country' and 'position'
        where position = 1 if the country supports Russia and 2 for Ukraine,
        finds the 5 most oriented countries in the two positions.

        Returns :
            The two top 5 of countries (lists) for Ukraine and Russia

        This function will be usefull if we add functionalities to our App that could potentially happen in a future update of our MVP.
        """
        # Creates 2 dataframes : one for each position (Ukraine or Russia)
        pro_ukraine_df = self.data[self.data["position"] == 2]
        pro_russia_df = self.data[self.data["position"] == 1]

        # Counts the number of tweets per country in each position
        ukr_counts = pro_ukraine_df["country"].value_counts()
        rus_counts = pro_russia_df["country"].value_counts()

        # Takes the top 5 of each count
        top_ukr_countries = ukr_counts.head(5).index.tolist()
        top_rus_countries = rus_counts.head(5).index.tolist()

        # Displays the tops
        print("Top 5 countries in support of Ukraine :", top_ukr_countries)
        print("Top 5 countries in support of Russia :", top_rus_countries)

    def extract_hashtags(self) -> None:
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

        # Convert JSON strings to Python lists
        self.data["hashtags"] = self.data["hashtags"].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else []
        )
        self.data["hashtags"] = self.data["hashtags"].apply(
            lambda x: [tag["text"] for tag in x] if isinstance(x, list) else []
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        This method is invoked when the `str()` function is called on an instance of the class.
        It returns a string representation of the 'data' attribute, which is the main DataFrame.

        Returns:
            str: A string representation of the DataFrame stored in the 'data' attribute.
        """
        return str(self.data)

    def get_number_pro_ukr_rus(self, is_pro_russian: bool):
        """
        Calculate the number of pro-Russian or pro-Ukrainian stances by country.

        This method groups the data by country and counts the number of instances
        aligning with either a pro-Russian or pro-Ukrainian stance, based on the
        'conflict_position' column in the dataset.

        Parameters:
        is_pro_russian (bool): A flag to determine the stance to be counted.
                            If True, counts pro-Russian stances.
                            If False, counts pro-Ukrainian stances.

        Returns:
        tuple: A tuple containing three lists:
            1. List of ISO country codes.
            2. List of counts of the specified stance (pro-Russian or pro-Ukrainian) per country.
            3. List of country names.
        """
        camp = 2
        if is_pro_russian:
            camp = 1

        # Grouping data by ISO and country, and counting the instances of the specified stance
        polarity_df = (
            self.data.groupby(["ISO", "country"])["conflict_position"]
            .apply(lambda x: (x == camp).sum())
            .reset_index()
        )
        # Filtering out rows where 'conflict_position' is NaN
        polarity_df = polarity_df[polarity_df["conflict_position"].notna()]

        # Extracting the list of ISO country codes, counts of specified stance, and country names
        iso_list = polarity_df["ISO"].tolist()
        polarity_list = polarity_df["conflict_position"].tolist()
        countries_list = polarity_df["country"].tolist()
        return iso_list, polarity_list, countries_list

    def getData(self) -> pd.DataFrame:
        """
        Retrieve the stored data.

        This method returns the DataFrame stored in the 'data' attribute of the class instance.

        Returns:
        pd.DataFrame: The DataFrame containing the stored data.
        """
        return self.data


