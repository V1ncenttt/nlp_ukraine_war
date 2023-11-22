
class TestModel(unittest.TestCase):

    def setUp(self):
        # Create a sample dataset for testing
        data = "data/tweets_processed/0402_UkraineCombinedTweetsDeduped_PROCESSED.csv"
        self.model = Model(data)

    def test_loadModel(self):
        # Test if the model is loaded successfully
        self.model.loadModel()
        self.assertIsNotNone(self.model.model)

    def test_apply_tweet_position(self):
        # Test if the tweet positions are applied correctly
        self.model.apply_tweet_position()
        self.assertIsNotNone(self.model.data['latitude'])
        self.assertIsNotNone(self.model.data['longitude'])

    def test_polarity(self):
        # Test the polarity calculation for a tweet
        tweet = 'I love Ukraine! #SlaviaUkraine'
        polarity = self.model.polarity(tweet)
        self.assertEqual(polarity, 2)

        tweet = 'I love bananas'
        polarity = self.model.polarity(tweet)
        self.assertEqual(polarity, 0)

        tweet = '#Azov are a nazi organisation. We need to denazify ukraine. #ZelenskiWarCriminal'
        polarity = self.model.polarity(tweet)
        self.assertEqual(polarity, 1)

    def test_get_average_polarity_for_country(self):
        # Test the calculation of average polarity for a country
        country = 'Ukraine'
        average_polarity = self.model.get_average_polarity_for_country(country)
        self.assertEqual(average_polarity, 0.5)

    def test_add_polarity(self):
        # Test if the polarity column is added correctly
        self.model.add_polarity()
        self.assertIn('polarity', self.model.data.columns)

    def test_add_sadness(self):
        # Test if the sadness column is added correctly
        self.model.add_sadness()
        self.assertIn('sadness', self.model.data.columns)

    def test_sort_by_favourite(self):
        # Test if the data is sorted by favorites correctly
        self.model.sort_by_favourite()
        self.assertEqual(self.model.data['favorites'].tolist(), [100, 75, 50])

    def test_sort_retweets(self):
        # Test if the data is sorted by retweets correctly
        self.model.sort_retweets()
        self.assertEqual(self.model.data['retweets'].tolist(), [300, 200, 100])

    def test_most_active_countries(self):
        # Test if the most active countries are calculated correctly
        most_active_countries = self.model.most_active_countries()
        self.assertEqual(most_active_countries, ['Ukraine', 'USA', 'Russia'])

    def test_most_active_user(self):
        # Test if the most active user is calculated correctly
        most_active_user = self.model.most_active_user()
        self.assertEqual(most_active_user, 'User1')

    def test_most_oriented_countries(self):
        # Test if the most oriented countries are calculated correctly
        most_oriented_countries = self.model.most_oriented_countries()
        self.assertEqual(most_oriented_countries, ['Ukraine', 'Russia'])

    def test_extract_hashtags(self):
        # Test if the hashtags are extracted correctly
        hashtags = self.model.extract_hashtags()
        self.assertEqual(hashtags, ['#Ukraine', '#War'])

    def test_get_number_pro_ukr_rus(self):
        # Test if the number of pro-Ukrainian or pro-Russian tweets is calculated correctly
        num_pro_ukr = self.model.get_number_pro_ukr_rus(is_pro_russian=False)
        num_pro_rus = self.model.get_number_pro_ukr_rus(is_pro_russian=True)
        self.assertEqual(num_pro_ukr, 1)
        self.assertEqual(num_pro_rus, 1)

    def test_getData(self):
        # Test if the data is returned correctly
        data = self.model.getData()
        self.assertEqual(data.shape, (3, 6))

if __name__ == '__main__':
    unittest.main()
import unittest
import pandas as pd
from model import Model
