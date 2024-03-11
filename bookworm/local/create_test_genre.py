# create_test_genre

import pandas as pd
f = "../data/genre.csv"
genres = pd.read_csv(f)
print(genres.shape)


test_genre = genres.head(30)
print(test_genre.shape)
print(test_genre.head)
f = "../data/test_data/test_genre.csv"
test_genre.to_csv(f)

genre_types = set(test_genre["generic_genre"].tolist())
print(genre_types)


