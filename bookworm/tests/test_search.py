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

test_semantic_search(self):
    Confirms semantic-search correctly calls get_semantic_results.

test_author_similar(self):
    Confirms that exact match queries return expected match. 

test_plot_semantic(self):
    Test plot_semantic_search against expected result.

test_author2_search_exact(self):
    Confirm author2_search returs books by that author only; exact match.

test_author2_search_close(self):
    Confirm author2_search returs books by that author only; close match.

test_author2_search_nomatch(self):
    Confirm error raised if no matching author.

test_genre_one_shot(self):
    Confirm genre search returns expected result.

test_genre_all:
    Confirm sum of all genres is sum of all rows in data.       

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
        f_embed = "data/test_data/test_data_w_embeddings.csv"
        self.test_dat_e = pd.read_csv(f_embed)
        f_ratings = "data/test_data/test_data.csv"
        self.test_dat_r = pd.read_csv(f_ratings)
        self.test_dat_filled = HelperFunctions.fill_na(self.test_dat_r)

        unfilled_data = {'author': ['Author1', None, 'Author3'],
                'book_title': ['Book1', None, 'Book3'],
                'genre': [None, 'Genre2', 'Genre3'],
                'summary': ['Summary1', 'Summary2', None]}
        self.test_dat_u = pd.DataFrame(unfilled_data)


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
        df = self.test_dat_e
        val_to_parse = df[df["book_id"] == 4081]["genre"][0]
        results = HelperFunctions.parse_genres(val_to_parse)
        expected = "Science Fiction, Speculative fiction"
        self.assertEqual(results, expected)


    def test_fill_na(self):
        """
        Confirm missing values in a df are correctly filled
        """

        filled_df = HelperFunctions.fill_na(self.test_dat_u)
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
        index = HelperFunctions.query_to_index(self.test_dat_e, query, columns)
        self.assertIsInstance(index, np.int64)

    @patch("search.HelperFunctions.fill_na")
    def test_query_to_index_calls_fill_na(self, mock_fill_na):
        """ 
        Confirm query_to_index correctly calls fill_na.
        """
        mock_fill_na.return_value = self.test_dat_filled
        columns = ["book_title"]
        HelperFunctions.query_to_index(self.test_dat_e, "dog", columns)
        mock_fill_na.assert_called_once_with(self.test_dat_e)


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
                query = self.test_dat_e[col][idx]
                expected = idx
                result = HelperFunctions.query_to_index(self.test_dat_e,
                                                query, [col])
            self.assertEqual(result, expected)


class TestSearch(unittest.TestCase):

    """
    Test cases for the Search Functions in Test Module
    """

    def setUp(self):
        """ 
        Creates and loads teating data. 
        """
        f_embed = "data/test_data/test_data_w_embeddings.csv"
        self.test_dat_e = pd.read_csv(f_embed)
        f_ratings = "data/test_data/test_data.csv"
        self.test_dat_r = pd.read_csv(f_ratings)
        f_genre = "data/test_data/test_genre.csv"
        self.test_data_g = pd.read_csv(f_genre)

    

    @patch("search.HelperFunctions.get_semantic_results")
    def test_semantic_search(self, mock_get):
        """
        Confirms semantic-search correctly calls get_semantic_results.
        """

        query = "Leviticus"
        f = "data/complete_w_embeddings/"
        f += "complete_w_embeddings.csv_part_1.csv"
        df = pd.read_csv(f)
        mock_get.return_value = [0, 1, 2, 3, 4]
        results = search.semantic_search(df, query, ["book_title"],
                                         num_books=5)
        for i in range(5):
            self.assertEqual(results.iloc[i]["book_title"], 
                             df.iloc[i]["book_title"])


    def test_author_similar(self):
        """
        Confirms that exact match queries return expected match.
        
        Pattern test. In any case where the query string is an exact 
        match to the author a book in the datset  
        we expect one of the top 3 books returned to be by that author.  Note:
        since keyword search is on all fields, some books returned may be by 
        other authors but with similar plots etc. For a search that returns 
        only books by the requested author, use author2 search.   
        """
        for idx in range(2):
            query = self.test_dat_e["author"][idx]
            books = search.author_similar_search(self.test_dat_e,
                                                 query, num_books=10)
            results = books["author"][0:2].tolist()
            expected = query
            self.assertIn(expected, results)


    def test_plot_semantic(self):
        """
        Test plot_semantic_search against expected result.
        
        One shot test. Using test data and a query that briefly 
        describes the plot of testbook_id 18560, "Leaf by Niggle", ensure 
        this book is returned as the top result."

        """
        query = "A man paints a tree."
        books = search.plot_semantic_search(self.test_dat_e,
                                            query, num_books=10)
        results = books.iloc[0]["book_id"]
        expected = self.test_dat_e.iloc[7]["book_id"] # 7=idx for Leaf by Niggle
        self.assertEqual(results, expected)



    def test_author2_search_exact(self):
        """ 
        Confirm author2_search returs books by that author only; exact match.

        Pattern test. In any case where the query string is an exact 
        match to the author field in dataset, ALL books returned should
        be by that author.  
 
        """

        for idx in [0,3,4,5,7,8,9]: #exclude rows with nan author
            query = self.test_dat_r["author"][idx]
            books = search.author2_search(self.test_dat_r, query, num_books=10)
            for idx2 in range(books.shape[0]):
                results = books.iloc[idx2]["author"]
                expected = query
                self.assertEqual(results, expected)

    def test_author2_search_close(self):
        """
        Confirm author2_search returs books by that author only; close match.
        
        One shot test. Search for author "JR Tolkien" to see if first
        book returned is by "J.R.R. Tolkien" as listed in test data. 
        """
        query = "JRR Tolkien"
        books = search.author2_search(self.test_dat_r, query, num_books=10)
        results = books.iloc[0]["author"]
        expected = "J. R. R. Tolkien"
        self.assertEqual(results, expected)

    def test_author2_search_nomatch(self):
        """
        Confirm error raised if no matching author.
        """
        query = "gribnif blah blah blah"
        with self.assertRaises(ValueError):
            search.author2_search(self.test_dat_r, query, num_books=10)

    def test_genre_one_shot(self):
        """ 
        Confirm genre search returns expected result.

        Using test data, genre search for "Horrer" should return
        one book, titled "The Queen of the Damned." 
        """
        df = self.test_data_g
        query = "Horror"
        results = search.genre_search(df, query).iloc[0]["book_title"]
        expected = "The Queen of the Damned"
        self.assertEqual(results,expected)

    def test_genre_all(self):
        """ Confirm sum of all genres is sum of dataset.
        
        Iterates over the rows in the test data. Counts the number
        of rows returned for each genre and sums the total. Expected
        total sum is the number of rows in the genre dataset.
        """
        df = self.test_data_g
        all_genres = set(df["generic_genre"])
        count = 0
        for genre in all_genres:
            results = search.genre_search(df, genre, num_books=df.shape[0])
            count += results.shape[0]
        expected = df.shape[0]
        self.assertEqual(count, expected)




if __name__ == '__main__':
    unittest.main()
