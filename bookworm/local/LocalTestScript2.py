# Sue's Local Search Script 

import pandas as pd
import search_wrapper as sw
import search
import numpy as np
from thefuzz import fuzz

#Assemble data 
path_root = "data/complete_w_embeddings/complete_w_embeddings.csv"
path1 = path_root + "_part_1.csv"
path2 = path_root + "_part_2.csv"
path3 = path_root + "_part_3.csv"
path4 = path_root + "_part_4.csv"
dat = sw.assemble_data(path1, path2, path3, path4)
col_to_show = ["book_id", "book_title", "author"]

print(dat[dat["book_id"] == 156489]["summary"])

indices = np.load('../bookworm/data/indices_updated.npy')
print(indices[0:5])

columns = ["book_title"]
query = "Harry Potter and the Order of the Phoenix"
book_index = search.HelperFunctions.query_to_index(dat, query, columns)
print(book_index)

print(dat.iloc[book_index][col_to_show])



semantic_indices = search.HelperFunctions.get_semantic_results(book_index,5)
semantic_indices = semantic_indices.tolist() if \
    isinstance(semantic_indices, np.ndarray) else semantic_indices

print(f"semantic indices are {semantic_indices}")
      
results = dat.loc[semantic_indices].head(5)
print(results)




# book = dat.iloc[0, :]
# id = book["book_id"]
# print(book)
# print(id)
# print(type(id))

# book2 = dat[dat["book_id"]== 4081]
# #book2 = dat[dat["book_id"]== 22808]
# #id2 = book2["book_id"]
# print(type(book2))
# #print(id2)

# #print(book[col_to_show].head(1))


# #book = dat[dat["book_id"] == 4081]
# # print(book)




