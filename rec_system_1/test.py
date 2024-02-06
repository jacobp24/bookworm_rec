from search import hybrid_search
import pandas as pd
import numpy as np

df = pd.read_csv("C:/Users/stlp/Desktop/Geeky/Software/bookworm_local/attempt_1/data_with_embeddings.csv")
distances = np.load('C:/Users/stlp/Desktop/Geeky/Software/bookworm_local/attempt_1/distances.npy')
indices = np.load('C:/Users/stlp/Desktop/Geeky/Software/bookworm_local/attempt_1/indices.npy')

print(hybrid_search(df,"God",distances, indices))