"""
This script loads datasets with embeddings, prepares the data for analysis,
sets up and applies a k-Nearest Neighbors (kNN) algorithm to find similar items
based on their embeddings, and saves/loads the inference results.
"""

# Corrected import order
import ast  # For safe evaluation of strings containing Python literals
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Load dataset
df1 = pd.read_csv("complete_w_embeddings.csv")

# Display dataframe columns for inspection
print(df1.columns)

def convert_embeddings_to_list(embeddings_series):
    """
    Converts string representations of embeddings in a pandas Series to lists.

    Parameters:
    - embeddings_series: A pandas Series containing string representations of embeddings.

    Returns:
    - A pandas Series containing the embeddings as lists.
    """
    return embeddings_series.apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Convert string representations of embeddings to lists
embeddings = convert_embeddings_to_list(df1['embeddings'])

# Convert embeddings to a NumPy array
X = np.array(embeddings.tolist())

print(f"Shape of the embeddings array: {X.shape}")

# Initialize and fit the k-Nearest Neighbors model
knn = NearestNeighbors(n_neighbors=21, metric='cosine')
knn.fit(X)

# Find the k-nearest neighbors for each point
distances, indices = knn.kneighbors(X)

# Save distances and indices for later use
np.save('distances_updated.npy', distances)
np.save('indices_updated.npy', indices)

# Load distances and indices
distances_loaded = np.load('distances_updated.npy')
indices_loaded = np.load('indices_updated.npy')

def print_most_similar_items(loaded_distances, loaded_indices, item_index=0, num_items=1):
    """
    Prints the most similar items based on the kNN analysis.

    Parameters:
    - loaded_distances: A NumPy array of distances between items, loaded from file.
    - loaded_indices: A NumPy array of indices of the nearest neighbors, loaded from file.
    - item_index: The index of the item for which to find similar items.
    - num_items: The number of similar items to display.
    """
    most_similar_index = loaded_indices[item_index][1]  # Skip the item itself
    similarity_score = 1 - loaded_distances[item_index][1]  # Convert distance to similarity
    print(f"Most similar plot index: {most_similar_index}")
    print(f"Similarity score: {similarity_score}")

    next_closest_indices = loaded_indices[item_index][1:num_items+1]
    similarity_scores = 1 - loaded_distances[item_index][1:num_items+1]
    print("Indices of the next closest items:", next_closest_indices)
    print(f"Similarity scores: {similarity_scores}")

# Example usage
print_most_similar_items(distances_loaded, indices_loaded, item_index=0, num_items=10)

print(f"Shape of the loaded distances array: {distances_loaded.shape}")
