import unittest
from unittest.mock import patch
from src.controller import Controller


class TestController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()

    def test_singleton(self):
        # Test the singleton pattern
        controller2 = Controller()
        self.assertEqual(self.controller, controller2)

    def test_get_all_countries(self):
        countries = self.controller.get_all_countries()
        self.assertIsNotNone(countries)
    
    def test_get_dates(self):
        # Test the get_dates method
        expected_dates = [
            "02/04",
            "08/04",
            "05/05 to 07/05",
            "19/08",
            "31/08",
            "08/09",
            "15/09",
        ]
        dates = self.controller.get_dates()
        self.assertEqual(dates, expected_dates)




