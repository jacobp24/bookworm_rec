"""
Script to create smaller test version of genres data. 

Module should be run from /scripts folder. 

"""

import pandas as pd
genres = pd.read_csv(f = "../data/genre.csv")
print(genres.shape)


test_genre = genres.head(30)
print(test_genre.shape)
print(test_genre.head)
test_genre.to_csv("../data/test_data/test_genre.csv")

genre_types = set(test_genre["generic_genre"].tolist())
print(genre_types)
