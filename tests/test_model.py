import unittest
import pandas as pd
from src.model import Model

class TestModel(unittest.TestCase):
    def setUp(self):
        # Create a sample dataset for testing
        data = "data/tweets_processed/0402_UkraineCombinedTweetsDeduped_PROCESSED.csv"
        self.model = Model(data)

    def test_get_average_polarity_for_country_invalid(self):
        # Test the calculation of average polarity for a country
        country = "Udegr"
        average_polarity = self.model.get_average_polarity_for_country(country)
        self.assertEqual(average_polarity, 0)
    
    def test_get_average_polarity_for_country_valid(self):
        country = "US"
        average_polarity = self.model.get_average_polarity_for_country(country)
        self.assertEqual(average_polarity, 0.25)

    def test_extract_hashtags(self):
        # Test if the hashtags are extracted correctly
        hashtags = self.model.data['hashtags']
        self.assertIsNotNone(hashtags)


    def test_getData(self):
        # Test if the data is returned correctly
        data = self.model.getData()
        self.assertIsNotNone(data)





