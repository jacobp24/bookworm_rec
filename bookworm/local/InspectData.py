# Sue's Local Search Script 

import pandas as pd
import search_wrapper as sw
import search
from search import HelperFunctions as H 
import numpy as np
from thefuzz import fuzz

#Assemble data 
path_root = "data/complete_w_embeddings/complete_w_embeddings.csv"
path1 = path_root + "_part_1.csv"
path2 = path_root + "_part_2.csv"
path3 = path_root + "_part_3.csv"
path4 = path_root + "_part_4.csv"
dat = sw.assemble_data(path1, path2, path3, path4)

col_to_show = ["book_id", "genre", "book_title", "author"]
#pd.set_option('display.max_colwidth', None) # display entire summary field
for query in ["Death at La Fenice", "Muder in Grub Street", "A touch of Frost"]:
    idx = H.query_to_index(dat, query, ["book_title"])
    print(f"Index is {idx}")
    book = dat.iloc[idx]
    for col in col_to_show:
        print(f"{col} is {book[col]}")
    print (book["summary"])
   


