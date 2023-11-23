import pandas as pd
import numpy as np
import re
import os
import pycountry
import geonamescache
import swifter
from functools import lru_cache
import torch
import ast
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm

class DataPreProcessor:
    """
    A class for preprocessing tweet data.

    This class is responsible for reading, cleaning, and transforming tweet data for analysis.
    It includes methods for geocoding, removing unnecessary columns, deleting links from tweets,
    and converting country names to ISO codes.

    Attributes:
        data (pd.DataFrame): DataFrame holding the tweet data.
        route (str): Path to the dataset file.
        cache (dict): Cache for storing geocoding results.
        gc (geonamescache.GeonamesCache): GeonamesCache instance for geocoding.
        countries (dict): Dictionary of country data from GeonamesCache.
        pc (pycountry.db): Pycountry database instance for country information.
    """

    def __init__(self, dataset: pd.DataFrame) -> None:
        self.data = pd.read_csv(dataset, low_memory=False).sample(20000)
        self.data = pd.read_csv(dataset, low_memory=False)

        self.route = dataset
        self.cache = {
            "New York": "USA",
            "England": "GBR",
            "NYC": "USA",
            "Boston": "USA",
        }
        self.data["location"] = self.data["location"].astype(str)
        self.gc = geonamescache.GeonamesCache()
        self.countries = self.gc.get_countries()
        self.pc = pycountry.countries
        self.loadModel()

    def loadModel(self) -> None:
        """
        Loads the pre-trained BERT model and tokenizer.

        Returns:
            None: Simply loads and prepares the model and tokenizer for use.
        """
        self.model = BertForSequenceClassification.from_pretrained(
            "../ml/model"
        )  # Load out pre-trained model
        self.tokenizer = BertTokenizer.from_pretrained("../ml/model")
        self.device = torch.device(
            "mps" if torch.backends.mps.is_available() else "cpu"
        )  # Optimise the model for the device
        self.model.to(self.device)
        self.model.eval()  # Load the model in eval/production mode

    
    def apply_tweet_position(self) -> None:
        """
        Classifies the text in the 'text' column of the instance's DataFrame using our pre-trained BERT model.

        This method tokenizes the text using the batch_encode_plus method of the tokenizer,
        processes it in batches using a DataLoader, and applies the pre-trained model to
        each batch to predict the sentiment/conflict position. The predictions are then
        appended to the DataFrame in a new column 'conflict_position'.
        Returns:
            None: Modifies the instance's DataFrame in place, adding a 'conflict_position' column with predictions.
        """
        tokens = self.tokenizer.batch_encode_plus(
            self.data["text"].tolist(),
            max_length=128,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )  # Tokenize the whole dataset

        dataset = TensorDataset(tokens["input_ids"], tokens["attention_mask"])
        dataloader = DataLoader(
            dataset, batch_size=64
        )  # Prepare the dataloader for batch processing

        positions = []
        with torch.no_grad():
            for batch in tqdm(dataloader, desc="Processing batches"):  # Make the predictions in batch
                input_ids, attention_mask = [
                    b.to(self.device) for b in batch
                ]  # Load the tensors in the selected device
                outputs = self.model(input_ids, attention_mask=attention_mask)
                logits = outputs.logits
                preds = torch.argmax(logits, dim=1).cpu().numpy()
                positions.extend(preds)

        # Add the predictions to the dataset
        self.data["conflict_position"] = positions

    @lru_cache(maxsize=None)
    def geocode(self, location: str) -> str:
        """
        Geocode a given location string to its country code.

        This method attempts to convert a location name into a country ISO code using various strategies,
        including a cache, splitting the location string, and using external libraries like pycountry
        and geonamescache.

        Args:
            location (str): The location string to be geocoded.

        Returns:
            str or None: The geocoded country ISO code or None if not found.
        """
        # Note: We use lru_cache to cache the results of this method to avoid repeated calls, which considerably speeds up the process
        if location == "nan" or len(location.split(" ")) > 3:
            return None

        loc = location.split(",")[0].strip()

        if location in self.cache:
            return self.cache[location]
        if loc in self.cache:
            return self.cache[loc]

        loc2 = location.split(",")[-1].strip()

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

    def geocode_helper(self, location: str) -> str:
        """
        Helper method for geocoding a location.

        This method assists the main geocode method by trying different strategies to find
        the country code of a given location string.

        Args:
            location (str): The location string to be geocoded.

        Returns:
            str or None: The geocoded country ISO code or None if not found.
        """

        try:
            country = self.countries[location]["iso"]
            return country

        except KeyError:
            try:
                countries = self.gc.get_cities_by_name(location)
                key = list(countries[0].keys())[0]
                country = countries[0][key]["countrycode"]
                return country
            except LookupError as e:
                return None
            except IndexError as e:
                return None

    def apply_geocode(self) -> None:
        """
        Apply geocoding to the 'location' column of the DataFrame.

        This method uses the geocode function to convert location names in the DataFrame
        to country ISO codes, storing the results in a new 'country' column.
        """

        self.data["country"] = self.data["location"].swifter.apply(
            lambda x: self.geocode(x)
        )

    @lru_cache(maxsize=None)
    def iso2_to_name(self, country_iso: str) ->str:
        try:
            nation = pycountry.countries.search_fuzzy(country_iso)[0]
            return nation.name
        except LookupError:
            # Handle the case where the country name is not found
            return None
        
    
    def apply_name(self) -> None:
        """
        Apply geocoding to the 'location' column of the DataFrame.

        This method uses the geocode function to convert location names in the DataFrame
        to country ISO codes, storing the results in a new 'country' column.
        """

        self.data["country"] = self.data["ISO"].swifter.apply(lambda x: self.iso2_to_name(x))

    @lru_cache(maxsize=None)
    def country_iso(self, country: str) -> str:
        """
        Convert a country name/ISO-2 to its ISO-3 code.

        Args:
            country (str): The country name to be converted.

        Returns:
            str or None: The ISO country code or None if not found.
        """

        # Note: We use lru_cache to cache the results of this method to avoid repeated calls, which considerably speeds up the process
        # List of all the countries found (some are None)
        if country == "xk":
            return "XKX"

        if country == "nan" or country == None:
            return None

        try:
            nation = pycountry.countries.search_fuzzy(country)[0]
            return nation.alpha_3
        except LookupError:
            # Handle the case where the country name is not found
            return None

    def apply_iso(self) -> None:
        """
        Apply ISO code conversion to the 'country' column of the DataFrame.

        This method uses the country_iso function to convert country names in the DataFrame
        to their ISO codes, storing the results in a new 'ISO' column.
        """

        self.data["ISO"] = self.data["country"].swifter.apply(
            lambda x: self.country_iso(x)
        )

    def delete_links(self) -> None:
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

    def remove_unnecessary_columns(self) -> None:
        """
        Remove unnecessary columns from the DataFrame.

        This method drops a predefined list of columns that are not needed for further analysis,
        simplifying the DataFrame.
        """

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

    def back_to_csv(self) -> None:
        """
        Save the processed DataFrame back to a CSV file.

        This method saves the cleaned and transformed DataFrame to a new CSV file,
        appending '_PROCESSED' to the original file name.
        """

        self.data.to_csv(
            "../data/tweets_processed/"
            + os.path.basename(self.route).replace(".csv", "")
            + "_PROCESSED.csv"
        )

    def preprocess_data(self) -> None:
        """
        Execute the full preprocessing pipeline on the tweet data.

        This method sequentially calls other methods in the class to perform various preprocessing
        steps like removing unnecessary columns, deleting links, applying geocoding, and converting
        country names to ISO codes. It also prints the progress of each step.
        """

        print("starting preprocessing for {}...".format(os.path.basename(self.route)))
        self.remove_unnecessary_columns()
        print("done removing unnecessary columns")
        self.delete_links()
        print("done deleting links")
        self.apply_geocode()
        print("done geocoding")
        self.apply_iso()
        self.apply_name()
        print('done applying iso')
        self.apply_tweet_position()
        print('done applying tweet position')
        self.back_to_csv()
        print("done preprocessing for {}".format(os.path.basename(self.route)))
        print("-----------------------------------")


if __name__ == "__main__":
    Data = [
        "../data/Tweets Ukraine/0408_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0402_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0505_to_0507_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0819_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0831_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0908_UkraineCombinedTweetsDeduped.csv",
        "../data/Tweets Ukraine/0915_UkraineCombinedTweetsDeduped.csv",
    ]
    for fichier in Data:
        D = DataPreProcessor(fichier)

        D.preprocess_data()

    print("Done creating all of the preprocessed files")
