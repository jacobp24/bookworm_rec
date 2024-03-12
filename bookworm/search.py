""" 
Module with search functions accross several modalities.

Includes helper functions as well as several search modes: 
    (1) semantic search - hybird keyword (TfidfVectorizer) and
        semantic (Voyeageai) search. Used for Author1 and Book_Title 
        search.
    (2) plot_semantic search based on voyageai semantic search
    (3) author2 search - fuzzy matching to author field 
    (4) genre search - exact matching to standardized genre field

Functions in TestHelperFunctions Class
==================================
parse_genres(genre_dict)
    Parse genre dictionaries into keywords joined by commas.

fill_na(df)
    Fill in missing values in dataframe with "unknown" or similar.

preprocess_text(text)
    Convert text to all lowercase.

get_semantic_results(df, query, columns, num_books=10)
    Extracts the indices of the closest books to given book_index.

query_to_index(df, query, columns, vectorizer=None)
    Maps query to the closest book index via keyword search.


Search Mode Functions
=====================

semantic_search(df, query, columns, num_books=10):
    Search for the closest books via keyword + semantic search. 

plot_semantic_search(df, query, num_books = 10):
    Search for closest set of books via pure semantic search.
    
author2_search(df, query, num_books=10):
    Search for closest set of books via fuzzy match on author field.

genre_search(data_frame, genre, num_books=10):
    Search for books within a specified genre and return the top-rated books.
"""

import os
import ast
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from thefuzz import fuzz
from dotenv import load_dotenv
import voyageai

# load environment variables from .env file
load_dotenv()

# load API for embeddings voyage
api_key = os.environ['API_KEY']

vo = voyageai.Client(api_key=api_key)

# load preprocessed distances/indices
try:
    distances = np.load('bookworm/data/distances_updated.npy')
except FileNotFoundError:
    distances = np.load('data/distances_updated.npy')
try:
    indices = np.load('bookworm/data/indices_updated.npy')
except FileNotFoundError:
    indices = np.load('data/indices_updated.npy')

class HelperFunctions:

    """
    Helper Functions used by main search functions
    """

    @staticmethod
    def parse_genres(genre_dict):
        """ 
        Parse genre dictionaries into keywords joined by commas.
        
        Paramters:
            Genres: A dictinonary of genres.
        Return
            A string with genres expressed as keywords, separated
            by commas.  
        """

        try:
            genres_dict = ast.literal_eval(genre_dict)
            genres_text = ', '.join(genres_dict.values())
        except (ValueError, SyntaxError):
            genres_text = 'Unknown Genre'
        return genres_text


    @staticmethod
    def fill_na(df):
        """ 
        Fill in missing values in dataframe

        Paramaters
            df: A dataframe with fields author, book_title, genre
                and summary. 
        Return: 
            A dataframe with missing values filled in. 
        """

        df.fillna({'author': 'Unknown', 'book_title': 'Unknown',
                   'genre': 'Unknown', 'summary': 'No Summary Available'},
                    inplace=True)
        return df

    @staticmethod
    def preprocess_text(text):
        """
        Convert text to all lowercase.
        
        Parameters:
            Text: A string
        Returns
            A lower case string
        """
        text = str(text).lower()
        return text

    @staticmethod
    def get_semantic_results(book_index, num_books=10):
        """
        Extracts indices of the closest books to given book_index.
        
        Indices extracted from global variable indices. Indices
        variables assumed to reflect closest books based on
        pre-processed semantic search.
        
        Parameters: 
            book_index: Int. The index of the book in the Indices 
                        param that is the base of the search.
            num_books:  Int. The number of indices to extract.
                        Default is 10. 
        Returns: 
            A numpy array of length num_books
        """
        similar_books_indices = indices[book_index][:num_books]
        return similar_books_indices

    @staticmethod
    def query_to_index(df, query, columns, vectorizer=None):
        """ 
        Maps query to the closest book index via keyword search.
        
        Maps query to the closest book in dataframe (df) 
        based on keyword search using given vectorizer(default
        is TfidfVectorizer). Then returns the index of that book
        in the dataframe.  Raises exception if no close match
        (consine similarity > .75).

        Parameters: 
            df:         A pandas dataframe, each row representing a book. 
                        Assumes df contains columns "book-title", "author",
                        "genre", and "summary." 

            query:      A string.  

            columns:    The columns to search over for the keyword search.

            vectorizer: Vectorizer to use to convert query for keyword search.
                        If none supplied TfidfVectorizer used. 
        Returns: 
            An np.int; the index of the closest book. 
        Exceptions:
            If no match (> .75 cosine similarity) raise ValueError.  
    """

        df = HelperFunctions.fill_na(df)
        df["genre"] = df['genre'].apply(HelperFunctions.parse_genres)
        df['combined_text'] = ''
        for index, row in df.iterrows():
            combined_text = ''
            for col in columns:
                new_txt = HelperFunctions.preprocess_text(str(row[col]))
                combined_text += new_txt + ' '
            df.at[index, 'combined_text'] = combined_text.strip()

        if vectorizer is None:
            vectorizer = TfidfVectorizer(stop_words='english')
            vectorizer.fit(df['combined_text'])
        query_vec = vectorizer.transform([query])
        cosine_similarities = linear_kernel(query_vec,
                vectorizer.transform(df['combined_text'])).flatten()
        most_relevant_index = cosine_similarities.argsort()[-1]
        best_distance = cosine_similarities[most_relevant_index]
        best_match = df.iloc[most_relevant_index][columns[0]]
        if best_distance < 0.75:
            err_msg = f"Sorry, we can't find that {columns[0]} in our database."
            # Offer suggestion if the best match had .5 < distance < .75
            if best_distance > 0.5:
                err_msg += f" Did you perhaps mean {best_match}?"
            err_msg += " You can also try searching by plot."
            raise ValueError(err_msg)
        return most_relevant_index


def semantic_search(df, query, columns, num_books=10):
    """ 
    Search for the closest books via keyword + embeddings search. 
    
    Maps query to the closest book (via keyword search), and then 
    retrieves the closest books based on pre-processed 
    semantic search distances. 

    Parameters: 
        df:         A pandas dataframe, each row representing a book. 
                    Assumes df contains columns "book-title", "author",
                    "genre", and "summary." 

        query:      A string.  

        columns:    The columns to search over during keyword search.

        num_books:  Int. The number of indices to extract. 
                    Defualt is 10.
    Returns: 
        A numpy array of length num_books.
    """

    book_index = HelperFunctions.query_to_index(df, query, columns)
    semantic_indices = HelperFunctions.get_semantic_results(book_index,
                                                            num_books)
    semantic_indices = semantic_indices.tolist() if \
        isinstance(semantic_indices, np.ndarray) else semantic_indices
    results = df.loc[semantic_indices].head(num_books)
    return results

def plot_semantic_search(df, query, num_books = 10):
    """
    Search for closest set of books via pure semantic search.

    Uses voyage-lite-02-instruct api to map query to a book
    in dataframe df based on semantic search.  Then selects
    closes set of books to matched book based on pre-computed
    semantic embeddings.

    Parameters: 
        df:     A pandas dataframe, each row representing a book. 
                
        query:  A string.  

        num_books:  Int. The number of books to extract. 
                    Defualt is 10.
    Returns: 
        A dataframe containing the selected books. 
    """
    # computing embeddings for the query
    query_embedding = vo.embed(query, model="voyage-lite-02-instruct",
                               input_type="document").embeddings

    # Convert embeddings from string representation back to lists
    # (and then to numpy arrays)
    embeddings_matrix = np.array([ast.literal_eval(embedding) if
            isinstance(embedding, str) else embedding for embedding
            in df['embeddings']])

    # Compute cosine similarities between the query embedding
    #and the book embeddings
    similarities = cosine_similarity(query_embedding, embeddings_matrix)

    # Get indices of the top N similar books
    top_n_indices = np.argsort(similarities[0])[::-1][:num_books]
    closest_books = df.iloc[top_n_indices]

    # Return the DataFrame containing the closest books
    return closest_books

def author2_search(df, query, num_books=10):

    """
    Search for closest set of books via fuzzy match on author field.

    Parameters: 
        df:     A pandas dataframe, each row representing a book. 
                Assumes df contains column "author".

        query:  A string. Value to serach for. 

        num_books:  Int. The number of books to extract. 
                    Defualt is 10.
    Returns: 
        A dataframe containing the selected books. 

    Exceptions:
        If no match on author field >.75, raise ValueError.      
    """
    #calculate match ratio
    df['ratio'] = df.apply(lambda row: fuzz.ratio(row['author'], query), axis=1)
    df_sorted = df.sort_values(by = "ratio",
                               ascending = False).reset_index(drop=True)


    # filter the database to only those rows with match > ratio
    result = df_sorted[df_sorted["ratio"] > 75]
    if result.empty:
        # Offer suggestions if there are matches with 50 < ratio < 75
        suggestions = []
        for idx in range(3):
            if df_sorted.iloc[idx]["ratio"] > 50:
                auth = df_sorted.iloc[idx]["author"]
                if not auth in suggestions:
                    suggestions.append(auth)

        err_msg = "That author does not appear in our database."
        if not suggestions:
            err_msg += " Perhaps you can try plot search."
        else:
            err_msg += " Perhaps you meant one of these authors: "
            for suggestion in suggestions:
                err_msg += f"{suggestion}, "
                err_msg = err_msg[:-2] + "?"

        raise ValueError(err_msg)

    results_sorted = result.sort_values(by='Book-Rating', ascending=False)
    results = results_sorted.head(num_books)
    return results

def genre_search(data_frame, genre, num_books=10):
    """
    Search for books within a specified genre and return the top-rated books.

    This function filters a DataFrame for books that match the specified genre,
    sorts these books by their rating,
    and returns the specified number of top-rated books within this genre.

    Parameters:
    - data_frame (pandas.DataFrame): The DataFrame containing book data.
    - genre (str): The genre to filter the books by.
    - num_books (int, optional): The number of top-rated books to return. 
        Defaults to 10.

    Returns:
    - pandas.DataFrame: A DataFrame containing the top-rated books within the 
        specified genre.
    """
    # Filter books by the specified genre
    filtered_books = data_frame[data_frame['generic_genre'] == genre]
    filtered_books = filtered_books.drop_duplicates(subset = "book_title")

    # Sort the filtered DataFrame by book rating in descending order
    # and select the top `num_books`
    top_rated_books =  filtered_books.sort_values(by='Book-Rating',
                            ascending=False).head(num_books)

    return top_rated_books
