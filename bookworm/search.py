import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from thefuzz import fuzz
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

import voyageai

# Load environment variables from .env file
load_dotenv()

# API for embeddings voyage
api_key = os.getenv("VOYAGE_API_KEY")
vo = voyageai.Client(api_key=api_key)

# Load data
# adding the df
# Read the first dataframe, which will provide the column names for the combined dataframe
df1 = pd.read_csv("bookworm/data/complete_w_embeddings/complete_w_embeddings.csv_part_1.csv")

# Read the remaining dataframes without adding their headers as column names
df2 = pd.read_csv("bookworm/data/complete_w_embeddings/complete_w_embeddings.csv_part_2.csv", header=None)
df3 = pd.read_csv("bookworm/data/complete_w_embeddings/complete_w_embeddings.csv_part_3.csv", header=None)
df4 = pd.read_csv("bookworm/data/complete_w_embeddings/complete_w_embeddings.csv_part_4.csv", header=None)
df2.columns = df1.columns
df3.columns = df1.columns
df4.columns = df1.columns

df = pd.concat([df1, df2, df3, df4], ignore_index=True)

distances = np.load('bookworm/data/distances_updated.npy')
indices = np.load('bookworm/data/indices_updated.npy')

class HelperFunctions:
    @staticmethod
    def parse_genres(genre_str):
        try:
            genres_dict = ast.literal_eval(genre_str)
            genres_text = ', '.join(genres_dict.values())
        except (ValueError, SyntaxError):
            genres_text = 'Unknown Genre'
        return genres_text

    @staticmethod
    def preprocess_text(text):
        text = str(text).lower()
        return text

    @staticmethod
    def get_semantic_results(book_index, num_books=10):
        similar_books_indices = indices[book_index][:num_books]
        return similar_books_indices

    @staticmethod
    def query_to_index(df, query, vectorizer=None):
        df.fillna({'author': 'Unknown', 'book_title': 'Unknown', 'genre': 'Unknown', 'summary': 'No Summary Available'}, inplace=True)
        df['combined_text'] = df.apply(lambda x: HelperFunctions.preprocess_text(f"{x['book_title']} {x['author']} {HelperFunctions.parse_genres(x['genre'])} {x['summary']}"), axis=1)
 
        if vectorizer is None:
            vectorizer = TfidfVectorizer(stop_words='english')
            vectorizer.fit(df['combined_text'])
        query_vec = vectorizer.transform([query])
        cosine_similarities = linear_kernel(query_vec, vectorizer.transform(df['combined_text'])).flatten()
        most_relevant_index = cosine_similarities.argsort()[-1]
        return most_relevant_index

def keyword_search(df, query, num_books=10):
    df.fillna({'author': 'Unknown', 'book_title': 'Unknown', 'genre': 'Unknown', 'summary': 'No Summary Available'}, inplace=True)
    df['combined_text'] = df.apply(lambda x: HelperFunctions.preprocess_text(f"{x['book_title']} {x['author']} {HelperFunctions.parse_genres(x['genre'])} {x['summary']}"), axis=1)
    query = HelperFunctions.preprocess_text(query)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['combined_text'])
    query_vec = vectorizer.transform([query])
    cosine_similarities = linear_kernel(query_vec, tfidf_matrix).flatten()
    top_book_indices = cosine_similarities.argsort()[-num_books:][::-1]

    keyword_results = df.iloc[top_book_indices]
    keyword_indices = keyword_results.index.tolist()
    results = df.loc[keyword_indices].head(num_books)
    return results

def semantic_search(df, query, num_books=10):
    book_index = HelperFunctions.query_to_index(df, query)
    semantic_indices = HelperFunctions.get_semantic_results(book_index, num_books)
    semantic_indices = semantic_indices.tolist() if isinstance(semantic_indices, np.ndarray) else semantic_indices
    results = df.loc[semantic_indices].head(num_books)
    return results

# Function for fuzzy matching for author2 search
def author2_search(df, query, ratio = 80, num_books=10):
   
    def calculate_ratio(row):
        return fuzz.ratio(row['author'], query)
    # Apply the function to each row and store the result in a new column
    df['ratio'] = df.apply(calculate_ratio, axis=1)
    # filter the database to only those rows with match > ratio
    result = df[df["ratio"] > ratio].tolist()
    results = result.head(num_books)
    
    return results

def plot_semantic_search(df, query, num_books = 10):
    # computing embeddings for the query
    query_embedding = vo.embed(query, model="voyage-lite-02-instruct", input_type="document").embeddings
    
    # Convert embeddings from string representation back to lists (and then to numpy arrays)
    embeddings_matrix = np.array([ast.literal_eval(embedding) if isinstance(embedding, str) else embedding for embedding in df['embeddings']])
    
    # Compute cosine similarities between the query embedding and the book embeddings
    similarities = cosine_similarity(query_embedding, embeddings_matrix)

    # Get indices of the top N similar books
    top_n_indices = np.argsort(similarities[0])[::-1][:num_books]
    closest_books = df.iloc[top_n_indices]
    
    # Return the DataFrame containing the closest books
    return closest_books
