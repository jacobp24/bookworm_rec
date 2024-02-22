from search import get_keyword_results as get_keyword_results
import pandas as pd
import numpy as np
from thefuzz import fuzz

df = pd.read_csv("data/complete_w_ratings.csv")
distances = np.load('data/distances.npy')
indices = np.load('data/indices.npy')

def filter(results, min_ave_ratings, min_num_rating):
    # Filter by min ave ratings if min >0.0
    # Otherwise keep all, including "none" values 
    if min_ave_ratings != 0.0:
        subset_df = results[results['Book-Rating'] > min_ave_ratings]
    else:
        subset_df = results
    
    # Filter by min num ratings if min_num >0
    # Otherwise keep all, including "none" values 
    if min_num_rating != 0:
        results_filtered = subset_df[subset_df['RatingCount'] > min_num_rating]
    else:
        results_filtered = subset_df
    return results_filtered

# Function for fuzzy matching for author2 search
def calculate_matching_ratio(df, query, ratio = 80):
   
    def calculate_ratio(row):
        return fuzz.ratio(row['author'], query)

    # Apply the function to each row and store the result in a new column
    df['ratio'] = df.apply(calculate_ratio, axis=1)
   

    # filter the database to only those rows with match > ratio
    result_df = df[df["ratio"] > ratio]
    
    
    return result_df


def search_wrapper(search_mode, search_value, min_ave_rating, min_num_ratings):
    if (search_mode == "Author2"):
        results = calculate_matching_ratio(df, search_value).head(10)
        print("Author2 mode")
        print(results.head())
    else: 
        results = get_keyword_results(df,search_value)
        print("other mode")
        print(results.head())
    print("Out of the if loop")
    print(results.head())
    results_filtered = filter(results, min_ave_rating, min_num_ratings)
    print(results_filtered.head())
    return results_filtered