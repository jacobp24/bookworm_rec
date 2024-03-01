import pandas as pd
import numpy as np

import ast

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

df = pd.read_csv("data/complete_w_ratings.csv")
#distances = np.load('data/distances.npy')
#indices = np.load('data/indices.npy')

def parse_genres(genre_str):
    try:
        # Safely evaluate the string as a dictionary
        genres_dict = ast.literal_eval(genre_str)
        # Extract genre names and join them into a single string
        genres_text = ', '.join(genres_dict.values())
    except (ValueError, SyntaxError):
        # Handle cases where the genre string is malformed or empty
        genres_text = 'Unknown Genre'
    return genres_text

# Function to preprocess text
def preprocess_text(text):
    """Basic text preprocessing"""
    text = str(text).lower()  # Convert NaN to 'nan' string, then lowercase text
    # Additional preprocessing here (e.g., remove punctuation, stopwords)
    return text

# Assuming df is your DataFrame containing the books dataset with modified 'genre'
def get_keyword_results(df, query, num_books=10):
    # Fill NaN values with a placeholder for other fields if necessary
    #df.fillna({'author_file1': 'Unknown', 'book_title_file1': 'Unknown', 'genre_file1': 'Unknown', 'summary_file1': 'No Summary Available'}, inplace=True)
    df.fillna({'author': 'Unknown', 'book_title': 'Unknown', 'genre': 'Unknown', 'summary': 'No Summary Available'}, inplace=True)

    # Combine text from different fields into a single text column
    #df['combined_text'] = (df['book_title_file1'] + ' ' + df['author_file1'] + ' ' + df['genre_file1'] + ' ' + df['summary_file1']).apply(preprocess_text)
    df['combined_text'] = (df['book_title'] + ' ' + df['author'] + ' ' + df['genre'] + ' ' + df['summary']).apply(preprocess_text)
    

    query = preprocess_text(query)
    
    # Use TF-IDF Vectorizer to transform texts into feature vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['combined_text'])
    
    # Vectorize the query
    query_vec = vectorizer.transform([query])
    
    # Compute the cosine similarity between query_vec and all book vectors
    cosine_similarities = linear_kernel(query_vec, tfidf_matrix).flatten()
    
    # Get the top N matching books
    top_book_indices = cosine_similarities.argsort()[-num_books:][::-1]
    
    return df.iloc[top_book_indices]

""" def get_semantic_results(book_index, num_books=10):
    # Fetch the indices of the most similar books for the given book index
    similar_books_indices = indices[book_index][:num_books]
    
    # Optionally, you might want to use distances to filter or sort the results further
    # For simplicity, this example returns the top N similar books directly
    
    return similar_books_indices """

""" def query_to_index(df, query, vectorizer=None):
    
    Map a search query to the most relevant book index in the dataset.

    :param df: DataFrame containing the books dataset.
    :param query: The search query as a string.
    :param vectorizer: Pre-fitted TF-IDF Vectorizer (optional).
    :return: Index of the most relevant book based on the query.
    
    # If a vectorizer is not provided, initialize and fit one based on the 'combined_text' column
    if vectorizer is None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        vectorizer.fit(df['combined_text'])

    # Vectorize the query using the provided or newly created vectorizer
    query_vec = vectorizer.transform([query])

    # Compute cosine similarity between the query vector and all book vectors
    from sklearn.metrics.pairwise import linear_kernel
    cosine_similarities = linear_kernel(query_vec, vectorizer.transform(df['combined_text'])).flatten()

    # Find the index of the most relevant book
    most_relevant_index = cosine_similarities.argsort()[-1]

    return most_relevant_index """

""" def hybrid_search(df, query, distances, indices, num_books=10, alpha=0.5):
    Perform a hybrid search combining keyword and semantic search results.

    :param df: DataFrame containing the books dataset.
    :param query: Search query string.
    :param distances: Numpy array of precomputed semantic distances.
    :param indices: Numpy array of precomputed semantic indices.
    :param num_books: Number of books to return.
    :param alpha: Weight for blending the results (0 to 1). Closer to 0 favors keyword, closer to 1 favors semantic.
    :return: DataFrame of the top N books based on hybrid search criteria.
    

    # Step 1: Perform Keyword-Based Search
    keyword_results = get_keyword_results(df, query, num_books)
    keyword_indices = keyword_results.index.tolist()
        
    # Step 2: Map query to an index for Semantic Search (this step is conceptual and needs a concrete implementation)
    # For demonstration, let's assume a function `query_to_index` that maps a query to an index for semantic search
    book_index = query_to_index(df, query)  # This function needs to be defined based on your application's specifics
    semantic_indices = get_semantic_results(book_index, num_books)
    semantic_indices = semantic_indices.tolist() if isinstance(semantic_indices, np.ndarray) else semantic_indices

    # Step 3: Combine Results
    # This could be a simple union or an intersection with weighted ranking
    combined_indices = list(set(keyword_indices + semantic_indices))
    
    # Optional: Re-rank combined results based on some criteria, e.g., blending scores
    # For simplicity, this example does not implement re-ranking

    # Fetch book details for the combined indices
    combined_results = df.loc[combined_indices].head(num_books)

    return combined_results
 """