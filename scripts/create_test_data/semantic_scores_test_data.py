""" 
Script creates preprocessed semantic indices and distances for test data.

Script intended to be run from /scripts folder.
"""

import ast
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

F = "../bookworm/data/test_data/test_data_w_embeddings.csv"
df = pd.read_csv(F)

# Convert String Representations to Lists
embeddings = df['embeddings'].apply(lambda x:
                    ast.literal_eval(x) if isinstance(x, str) else x)

# Convert to numpy array
X = np.array(embeddings.tolist())

# Perform knn
knn = NearestNeighbors(n_neighbors=min(X.shape[0], 21), metric='cosine')
knn.fit(X)

# Find the k-nearest neighbors for each point
distances, indices = knn.kneighbors(X)

# Save results as np arrays
np.save("../bookworm/data/test_data/distances_test.npy", distances)
np.save("../bookworm/data/test_data/indices_test.npy", indices)

# Also print to csv files
# For easy visual inspection to facilitate testing
indices_df = pd.DataFrame(indices)
F2 = "../bookworm/data/test_data/indices_test.csv"
indices_df.to_csv(F2)
#print(indices_df.head())

distances_df = pd.DataFrame(distances)
F3 = "../bookworm/data/test_data/distances_test.csv"
distances_df.to_csv(F3)
#print(distances_df.head())
