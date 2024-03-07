"""
Module: test_search


This module contains unit tests for the search module. 

The tests are organized into a TestCase class named TestSear

Test Cases:

Dependencies:
- unittest: The built-in unit testing framework in Python.
- patch: A utility from the unittest.mock module used for mocking objects
    during testing.
- pandas: A library for data manipulation and analysis.

Usage:
Run this module to execute the unit tests for the search modules. 

"""

import unittest
from unittest.mock import patch
import pandas as pd
from bookworm.search import HelperFunctions



class TestSearch(unittest.TestCase):
    """Test cases for the TestWrapper Module """
    
    def test_preprocess_text(self):
        results = HelperFunctions.preprocess_text("UPPERandlower74")
        self.assertEqual(results, "upperandlower74")

    #def test_parse_genres_full(self):
        #results = HelperFunctions.parse_genres()
    
    def test_parse_genres_empty(self):
        results = HelperFunctions.parse_genres("")
        self.assertEqual(results, "Unknown Genre")

    #def test_query_to_index(self):
        #results = HelperFunctions.query_to_index


    

if __name__ == '__main__':
    unittest.main()