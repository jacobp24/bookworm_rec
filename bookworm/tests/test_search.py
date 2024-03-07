"""
Module: test_search


This module contains unit tests for the search module. 

The tests are organized into two classes TestHelperFunctions and
TestSearchFunctions

Test Cases in TestHelperFunctions
=================================
test_preprocess_text(self):
    Confirm preprocess_text function converts to lowercase

test_parse_genres_empty(self):
    Confirm empty genre field populated with "Unknown Genre".

test_parse_genres_full(self):
    Confirm proper parsing of genre dictionary.

test_fill_na(self):
    Confirm missing values in a df are correctly filled

test_get_semantic_results(self):
    Confirm that function extracts proper indices.

test_query_to_index_smoke(self):
    Confirm query_to_index function returns an np integer.

test_query_to_index_calls_fill_na(self, mock_fill_na):
    Confirm query_to_index correctly calls fill_na.

test_query_exact(self):
    Confirms that exact match queries return expected match.


    
    

Dependencies:
- unittest: The built-in unit testing framework in Python.
- pandas: A library for data manipulation and analysis.
- numpy: A library for numerical manipulation.

Usage:
Run this module to execute the unit tests for the search module. 

"""
import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
import os
from search import HelperFunctions


class TestHelperFunctions(unittest.TestCase):
    """
    Test cases for the Helper Functions in TestWrapper Module
    """

    def setUp(self):
        """ 
        Creates and loads teating data. 
        """
        try: 
            f = "data/test_data.csv"
            self.test_dat = pd.read_csv(f)
        except: 
            f = "bookworm/data/test_data.csv"
            self.test_dat = pd.read_csv(f)
            

        self.test_dat_filled = HelperFunctions.fill_na(self.test_dat)

        unfilled_data = {'author': ['Author1', None, 'Author3'],
                'book_title': ['Book1', None, 'Book3'],
                'genre': [None, 'Genre2', 'Genre3'],
                'summary': ['Summary1', 'Summary2', None]}
        self.test_dat2 = pd.DataFrame(unfilled_data)


    def test_preprocess_text(self):
        """
        Confirm preprocess_text function converts to lowercase
        """
        results = HelperFunctions.preprocess_text("UPPERandlower74")
        self.assertEqual(results, "upperandlower74")


    def test_parse_genres_empty(self):
        """
        Confirm empty genre field populated with "Unknown Genre".
        """
        results = HelperFunctions.parse_genres("")
        self.assertEqual(results, "Unknown Genre")

    def test_parse_genres_full(self):
        """
        Confirm proper parsing of genre dictionary." 

        Using book-ID = 4081 from test_data, expected result
        is "Science Fiction, Speculative fiction".
        """
        df = self.test_dat
        val_to_parse = df[df["book_id"] == 4081]["genre"][0]
        results = HelperFunctions.parse_genres(val_to_parse)
        expected = "Science Fiction, Speculative fiction"
        self.assertEqual(results, expected)


    def test_fill_na(self):
        """
        Confirm missing values in a df are correctly filled
        """

        filled_df = HelperFunctions.fill_na(self.test_dat2)
        self.assertEqual(filled_df.isnull().sum().sum(), 0)
        self.assertEqual(filled_df['author'].iloc[1], 'Unknown')
        self.assertEqual(filled_df['book_title'].iloc[1], 'Unknown')
        self.assertEqual(filled_df['genre'].iloc[0], 'Unknown')
        self.assertEqual(filled_df['summary'].iloc[2], 'No Summary Available')

    def test_get_semantic_results(self):
        """
        Confirm that function extracts proper indices.
        
        get_semantic_results is a function that extracts the indices
        of the closest books, based on semantic distance from a given
        book identifed by index, from a file in which the indices are 
        stored. Testing with existing indice_updated.npy data, 
        ensure the proper row is extracted. For book_index 2, 
        and num_books = 3, the function should 
        return [11478, 7476, 10642]
        
        """
        results = HelperFunctions.get_semantic_results(2, num_books=3)
        expected = np.array([11478, 7476, 10642])
        self.assertEqual(results.all(), expected.all())

    def test_query_to_index_smoke(self):
        """ 
        Confirm query_to_index function returns an np integer.
        """
        query = "sample query"
        index = HelperFunctions.query_to_index(self.test_dat, query)
        self.assertIsInstance(index, np.int64)

    @patch("search.HelperFunctions.fill_na")
    def test_query_to_index_calls_fill_na(self, mock_fill_na):
        """ 
        Confirm query_to_index correctly calls fill_na.
        """
        mock_fill_na.return_value = self.test_dat_filled
        HelperFunctions.query_to_index(self.test_dat, "dog")
        mock_fill_na.assert_called_once_with(self.test_dat)
    

    def test_query_exact(self):
        """
        Confirms that exact match queries return expected match
        
        Pattern test. In any case where the query string is an exact 
        and uniquematch to something in a given row of the test data, we
        expect the relevant row to be returned as the match. 
        """
        for idx in [0, 10]:
            for query in [self.test_dat["summary"][idx],
                          self.test_dat["book_title"][idx]]:
                expected = idx
                result = HelperFunctions.query_to_index(self.test_dat, query)
                self.assertEqual(result, expected)


    # def test_select_search(self):
    #     f = "bookworm/data/test_data.csv"
    #     test_dat = pd.read_csv(f)
    #     results = search_wrapper.select_search(test_dat, "Author2",
    #                                            "J. R. Tolkien", 0.0, 0)
    #     self.assertEqual(results.shape[0], 2)

if __name__ == '__main__':
    unittest.main()
