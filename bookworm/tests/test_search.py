"""
Module: test_search


This module contains unit tests for the search module. 

The tests are organized into two classes TestHelperFunctions and
TestSearchFunctions

Test Functions in TestHelperFunctions Class
===========================================
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

Test Functions in TestSearch Class
======================================    

test_plot_semantic(self):
    Test plot_semantic_search against expected result.

test_keyword_close(self):
    Confirms that close match queries return expected match.

test_keyword_exact(self):
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
try:
    import search
    from search import HelperFunctions
except ImportError:
    from bookworm import search
    from bookworm.search import HelperFunctions

class TestHelperFunctions(unittest.TestCase):
    """
    Test cases for the Helper Functions in Search Module
    """

    def setUp(self):
        """ 
        Creates and loads teating data. 
        """
        try:
            f = "data/test_data_w_embeddings.csv"
            self.test_dat = pd.read_csv(f)
        except ImportError:
            f = "bookworm/data/test_data_w_embeddings.csv"
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
        query = "Book of Job"
        columns = ["book_title"]
        index = HelperFunctions.query_to_index(self.test_dat, query, columns)
        self.assertIsInstance(index, np.int64)

    @patch("search.HelperFunctions.fill_na")
    def test_query_to_index_calls_fill_na(self, mock_fill_na):
        """ 
        Confirm query_to_index correctly calls fill_na.
        """
        mock_fill_na.return_value = self.test_dat_filled
        columns = ["book_title"]
        HelperFunctions.query_to_index(self.test_dat, "dog", columns)
        mock_fill_na.assert_called_once_with(self.test_dat)


    def test_query_exact(self):
        """
        Confirms that exact match queries return expected match
        
        Pattern test. In any case where the query string is an exact 
        and unique match to something in a given row of the test data, we
        expect the relevant row to be returned as the match. 
        """
        columns = ["book_title", "author", "genre"]
        for col in columns:
            for idx in [0, 10]:
                query = self.test_dat[col][idx]
                expected = idx
                result = HelperFunctions.query_to_index(self.test_dat,
                                                query, [col])
            self.assertEqual(result, expected)


class TestSearch(unittest.TestCase):
    """
    Test cases for the Search Functions in Test Module
    """
    def setUp(self):
        """ 
        Creates and loads testing data. 
        """
        try:
            f = "data/test_data_w_embeddings.csv"
            self.test_dat = pd.read_csv(f)
        except ImportError:
            f = "bookworm/data/test_data_w_embeddings.csv"
            self.test_dat = pd.read_csv(f)


    def test_keyword_exact(self):
        """
        Confirms that exact match queries return expected match
        
        Pattern test. In any case where the query string is an exact 
        and unique match to the title of a book in the datset  
        we expect the first book returned to be the exact match. 
        """
        for idx in range(2):
            query = self.test_dat["book_title"][idx]
            books = search.keyword_search(self.test_dat, query, num_books=10)
            results = books.iloc[0]["book_title"]
            expected = query
            self.assertEqual(results, expected)


    def test_author2_search_exact(self):
        """ 
        Confirm author2_search returs books by that author only; exact match.

        Pattern test. In any case where the query string is an exact 
        match to the author field in dataset, ALL books returned should
        be by that author.  
 
        """

        for idx in [0,3,4,5,7,8,9]: #exclude rows with nan author
            query = self.test_dat["author"][idx]
            books = search.author2_search(self.test_dat, query, num_books=10)
            for idx2 in range(books.shape[0]):
                results = books.iloc[idx2]["author"]
                expected = query
                self.assertEqual(results, expected)

    def test_author2_search_close(self):
        """
        Confirm author2_search returs books by that author only; close match.
        
        One shot test. Search for author "JR Tolkien" to see if first
        book return is by "J.R.R. Tolkien" as listed in test data. 
        """
        query = "JRR Tolkien"
        books = search.author2_search(self.test_dat, query, num_books=10)
        results = books.iloc[0]["author"]
        expected = "J. R. R. Tolkien"
        self.assertEqual(results, expected)

    def test_author2_search_nomatch(self):
        """
        Confirm error raised if no matching author.
        """
        query = "gribnif blah blah blah"
        with self.assertRaises(ValueError):
            search.author2_search(self.test_dat, query, num_books=10)

    def test_plot_semantic(self):
        """
        Test plot_semantic_search against expected result.
        
        One shot test. Using test data and a query that briefly 
        describes the testbook_id 18560, "Leaf by Niggle", ensure 
        this book is returned as the top result."

        """
        query = "A man paints a tree."
        books = search.plot_semantic_search(self.test_dat, query, num_books=10)
        results = books.iloc[0]["book_id"]
        expected = self.test_dat.iloc[7]["book_id"] # 7 = idx for Leaf by Niggle
        # print(self.test_dat[self.test_dat["book_id"] == 18560])
        self.assertEqual(results, expected)

    # def test_semantic(self):
    #     """
    #     Test semantic_search against expected result.

    #     Using test data and a query that briefly describes the test
    #     book_id 18560, "Leaf by Niggle", ensure this book is returned
    #     as the top result."
    #     """
    #     query = " Leaf by Niggle"
    #     columns = ["book_title"]
    #     with patch('search.indices', test_indices):  # TO DO: MAKE THESE
    #     books = search.semantic_search(self.test_dat, query, columns, num_books=10)
    #     books = search.semantic_search(self.test_dat, query, columns, num_books=10)
    #     results = books.iloc[0]["book_id"]
    #     expected = self.test_dat.iloc[7]["book_id"] # 7 = idx for Leaf by Niggle
    #     self.assertEqual(results, expected)


if __name__ == '__main__':
    unittest.main()
