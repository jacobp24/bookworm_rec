# %%
import pandas as pd
import numpy as np

import ast  # Safe evaluation of strings containing Python literals

from sklearn.neighbors import NearestNeighbors

# %%
df = pd.read_csv("data_with_embeddings.csv")
df1 = pd.read_csv("complete_w_embeddings.csv")

# %%
df.columns

# %%
df1.columns

# %%
# Convert String Representations to Lists
embeddings = df1['embeddings'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# %%
# Converting to numpy array
X = np.array(embeddings.tolist())

# %%
X.shape

# %%
# setting up the kNN
knn = NearestNeighbors(n_neighbors=21, metric='cosine')

# %%
knn.fit(X)

# %%
# Find the k-nearest neighbors for each point
distances, indices = knn.kneighbors(X)

# %% [markdown]
# # Inference

# %%
np.save('distances_updated.npy', distances)
np.save('indices_updated.npy', indices)

# %%
distances_loaded = np.load('distances_updated.npy')
indices_loaded = np.load('indices_updated.npy')

# %%
# First plot inference
most_similar_index = indices_loaded[0][1]  # [0] for the first plot, [1] to skip the plot itself
similarity_score = 1 - distances_loaded[0][1]  # Convert distance to similarity

print(f"Most similar plot index: {most_similar_index}")
print(f"Similarity score: {similarity_score}")

# %%
next_10_closest_indices = indices[0][1:11]
similarity_score = 1 - distances_loaded[0][1:11]

print("Indices of the next 10 closest items:", next_10_closest_indices)
print(f"Similarity score: {similarity_score}")

# %%
distances_loaded.shape

# %%



