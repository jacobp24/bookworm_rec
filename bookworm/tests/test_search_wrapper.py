"""
Module: test_search_wrapper


This module contains unit tests for the search and filter functions
implemented in the search_warpper.py module. 

The tests are organized into four Test Classes each corresponding to a
function in the search modules to be tested. 

Tests in Class TestFilter
==========================

test_filter_min_ave_ratings(self):
    Confirm that filter_ratings() properly filters by average ratings. 

test_filter_min_num_ratings(self):
    Confirm filter_ratings() properly filters by number ratings.

test_filter_no_mins(self):
    Confirm filter_ratings() returns all values when no mins set.  

test_filter_missing_col1(self):
    Confirm ValueError raised if no Book-Rating colum.



Tests in Class TestSelectSearch
===============================
test_select_search_author2(self, mock_author2_search):
    Confirm correct search function called for search_mode Author2

test_select_search_title(self, mock_semantic_search):
    Confirm correct search function called for search_mode Title

test_select_search_plot(self, mock_plot_semantic_search):
    Confirm correct search function called for search_mode plot

test_select_search_author1(self, mock_plot_keyword_search):
    Confirm correct search function called for search_mode author1

test_select_search_genre(self, mock_plot_keyword_search):
    Confirm correct search function called for search_mode Genre

Tests in Class TestAssembleData
===============================
test_assemble_data_correct_shape(self):
    Test to ensure final df is expected shape.

test_assemble_data_smoke_test(self):
    Test to ensure the assembled data is a datframe

Tests in Class TestSearchWrapper
===============================
def test_wrapper_calls_filter(self, mock_select_search):
    Smoke test for search_wrapper
        


Dependencies:
- unittest: The built-in unit testing framework in Python.
- patch: A utility from the unittest.mock module used for mocking objects
    during testing.
- pandas: A library for data manipulation and analysis.

Usage:
Run this module to execute the unit tests for the search_wrapper modules. 

"""

import unittest
from unittest import mock
import pandas as pd
# pylint: disable=consider-using-from-import
# pylint: disable=import-error
import bookworm.search_wrapper as search_wrapper

class TestFilter(unittest.TestCase):
    """Test cases for the filter_ratings function"""

    def test_filter_min_ave_ratings(self):
        """ 
        Confirm that filter_ratings() properly filters by average ratings. 
         
        Using test data as input and setting average ratings filter to
        6 should result in 2 entries remaining after filtering. 
        """
        f = "bookworm/data/test_data.csv"
        test_dat = pd.read_csv(f)
        results = search_wrapper.filter_ratings(test_dat, 6, 0)
        self.assertEqual(results.shape[0], 2)

    def test_filter_min_num_ratings(self):
        """ 
        Confirm filter_ratings() properly filters by number ratings.
         
        Using test data as input and setting number of ratings filter 
        to 6 should result in 1 entry remaining after filtering. 
        """
        f = "bookworm/data/test_data.csv"
        test_dat = pd.read_csv(f)
        results = search_wrapper.filter_ratings(test_dat, 0, 6)
        self.assertEqual(results.shape[0], 1)

    def test_filter_no_mins(self):
        """ 
        Confirm filter_ratings() returns all values when no mins set. 
        
        Using test data as input and setting min and average ratings
        filter to zero should return data in same shape as original
        data.
        """
        f = "bookworm/data/test_data.csv"
        test_dat = pd.read_csv(f)
        results = search_wrapper.filter_ratings(test_dat, 0, 0)
        self.assertEqual(results.shape[0], test_dat.shape[0])

    def test_filter_missing_col1(self):
        """
        Confirm ValueError raised if no Book-Rating colum.
        """
        test_dat = pd.DataFrame([[0,0], [0,0]])
        test_dat.columns = ["First column", "RatingCount"]
        with self.assertRaisesRegex(ValueError,
                    "Your data must have a Book-Ratings column"):
            search_wrapper.filter_ratings(test_dat, 0,0)

    def test_filter_missing_col2(self):
        """
        Confirm ValueError raised if no Book-Rating colum.
        """
        test_dat = pd.DataFrame([[0,0], [0,0]])
        test_dat.columns = ["Book-Rating", "foo"]
        with self.assertRaisesRegex(ValueError,
                    "Your data must have a RatingCount column"):
            search_wrapper.filter_ratings(test_dat, 0,0)

class TestSelectSearch(unittest.TestCase):
    """Test cases for the filter_ratings function"""

    @mock.patch("bookworm.search.author2_search")
    def test_select_search_author2(self, mock_author2_search):
        """
        Confirm correct search function called for search_mode Author2
        """
        f = "bookworm/data/test_data.csv"
        test_dat = pd.read_csv(f)
        mock_author2_search.return_value = "Author2 search performed"
        results = search_wrapper.select_search(test_dat, "Author2",
                                               "J. R. Tolkien")
        self.assertEqual(results, "Author2 search performed")

    @mock.patch("bookworm.search.semantic_search")
    def test_select_search_title(self, mock_semantic_search):
        """
        Confirm correct search function called for search_mode Title
        """
        f = "bookworm/data/test_data.csv"
        test_dat = pd.read_csv(f)
        mock_semantic_search.return_value = "Semantic search performed"
        results = search_wrapper.select_search(test_dat, "Title",
                                               "J. R. Tolkien")
        self.assertEqual(results, "Semantic search performed")

    @mock.patch("bookworm.search.plot_semantic_search")
    def test_select_search_plot(self, mock_plot_semantic_search):
        """
        Confirm correct search function called for search_mode Plot
        """
        f = "bookworm/data/test_data.csv"
        test_dat = pd.read_csv(f)
        mock_plot_semantic_search.return_value = "Plot search performed"
        results = search_wrapper.select_search(test_dat, "Plot",
                                               "J. R. Tolkien")
        self.assertEqual(results, "Plot search performed")

    @mock.patch("bookworm.search.keyword_search")
    def test_select_search_author1(self, mock_keyword_search):
        """
        Confirm correct search function called for search_mode Author1
        """
        f = "bookworm/data/test_data.csv"
        test_dat = pd.read_csv(f)
        mock_keyword_search.return_value = "Keyword search performed"
        results = search_wrapper.select_search(test_dat, "Author1",
                                               "J. R. Tolkien")
        self.assertEqual(results, "Keyword search performed")

    @mock.patch("bookworm.search.keyword_search")
    def test_select_search_genre(self, mock_keyword_search):
        """
        Confirm correct search function called for search_mode genre
        """
        f = "bookworm/data/test_data.csv"
        test_dat = pd.read_csv(f)
        mock_keyword_search.return_value = "Keyword search performed"
        results = search_wrapper.select_search(test_dat, "Genre",
                                               "J. R. Tolkien")
        self.assertEqual(results, "Keyword search performed")

class TestAssembleData(unittest.TestCase):
    """Test cases for the assemble_data function"""

    def define_paths(self):
        """
        Helper function; creates mock paths for assemble_function tests
        """
        path1 = "bookworm/data/test_data.csv"
        path2 = "bookworm/data/test_data2.csv"
        path3 = "bookworm/data/test_data3.csv"
        path4 = "bookworm/data/test_data3.csv"
        return (path1, path2, path3, path4)

    def test_assemble_data_smoke_test(self):
        """
        Test to ensure the assembled data is a datframe
        """
        p1, p2, p3, p4 = self.define_paths()
        results=search_wrapper.assemble_data(p1, p2, p3, p4)
        self.assertIsInstance(results, pd.DataFrame)

    def test_assemble_data_correct_shape(self):
        """
        Test to ensure final df is expected shape.     
        """
        p1, p2, p3, p4 = self.define_paths()
        results=search_wrapper.assemble_data(p1, p2, p3, p4)
        d1 = pd.read_csv(p1)
        d2 = pd.read_csv(p2)
        d3 = pd.read_csv(p3)
        d4 = pd.read_csv(p4)
        expected_rows = d1.shape[0] + d2.shape[0] + d3.shape[0] + d4.shape[0]
        self.assertEqual(results.shape[0], expected_rows)

class TestSearchWrapper(unittest.TestCase):
    """
    Test cases for the search_wrapper function
    """
    @mock.patch("bookworm.search_wrapper.select_search")
    def test_wrapper_calls_filter(self, mock_select_search):
        """
        Smoke test for search_wrapper
        """
        f = "bookworm/data/test_data.csv"
        test_dat = pd.read_csv(f)
        # Assume the search function returns the original data
        mock_select_search.return_value = test_dat
        # call search wrapper
        results = search_wrapper.search_wrapper("Title", "Goofy", 6, 0)
        # results should be the original test_dat (no filters)
        # call filter function on test and min-ratings, 6
        # expected result is 2 entries
        self.assertEqual(results.shape[0], 2)


if __name__ == '__main__':
    unittest.main()
