import search
import pandas as pd
import numpy as np
from thefuzz import fuzz

# adding the df
# Read the first dataframe, which will provide the column names for the combined dataframe
df1 = pd.read_csv("data/complete_w_embeddings/complete_w_embeddings.csv_part_1.csv")

# Read the remaining dataframes without adding their headers as column names
df2 = pd.read_csv("data/complete_w_embeddings/complete_w_embeddings.csv_part_2.csv", header=None)
df3 = pd.read_csv("data/complete_w_embeddings/complete_w_embeddings.csv_part_3.csv", header=None)
df4 = pd.read_csv("data/complete_w_embeddings/complete_w_embeddings.csv_part_4.csv", header=None)
df2.columns = df1.columns
df3.columns = df1.columns
df4.columns = df1.columns

df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Filter
def filter(results, min_ave_ratings, min_num_rating):
    # Filter by min ave ratings if min > 0.0
    # Otherwise keep all, including "none" values 
    if min_ave_ratings != 0.0:
        subset_df = results[results['Book-Rating'] > min_ave_ratings]
    else:
        subset_df = results
    
    # Filter by min num ratings if min_num > 0
    # Otherwise keep all, including "none" values 
    if min_num_rating != 0:
        results_filtered = subset_df[subset_df['RatingCount'] > min_num_rating]
    else:
        results_filtered = subset_df
    return results_filtered

def search_wrapper(search_mode, search_value, min_ave_rating, min_num_ratings, num_books=10):
    if (search_mode == "Author2"):
        results = search.author2_search(df, search_value, num_books)
    if (search_mode == "Title"):
        results = search.semantic_search(df, search_value, num_books)
    if (search_mode == "Plot"):
        results = search.plot_semantic_search(df, search_value, num_books)
    else: 
        results = search.keyword_search(df, search_value, num_books)
    results_filtered = filter(results, min_ave_rating, min_num_ratings)
    return results_filtered