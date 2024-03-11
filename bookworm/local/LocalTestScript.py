# Sue's Local Search Script 

import pandas as pd
import search_wrapper as sw
import search
from thefuzz import fuzz

#Assemble data 
path_root = "data/complete_w_embeddings/complete_w_embeddings.csv"
path1 = path_root + "_part_1.csv"
path2 = path_root + "_part_2.csv"
path3 = path_root + "_part_3.csv"
path4 = path_root + "_part_4.csv"
dat = sw.assemble_data(path1, path2, path3, path4)

col_to_show = ["book_id", "book_title", "author"]
ALL_COL = ["genre", "book_title", "summary", "author"]

def calculate_ratio(row):
        return fuzz.ratio(row['author'], query)

#print(dat[col_to_show].iloc[15:40])

# authors_to_check = ["Herge", "Isaac Asimov", "Asimov", "Tarkington", "Stephen King", 
#                     "JRR Tolkien", "Tolkien", "Rowling", "Joyce", "James Joyce"]
# # results from keyword author field only
# for author in authors_to_check:
#     idx = search.HelperFunctions.query_to_index(dat, author, ["author"])
#     auth_result = dat.iloc[idx]["author"]
#     print(f"For author {author}, index is {idx} and author is {auth_result}")

# # results from keyword all fields
# for author in authors_to_check:
#     columns = ["book_title", "genre", "author", "summary"]
#     idx = search.HelperFunctions.query_to_index(dat, author, columns)
#     auth_result = dat.iloc[idx]["author"]
#     print(f"For author {author}, index is {idx} and author is {auth_result}")

books_to_check = ["way of all flesh", "wizard and glass", "winters heart", "winter's heart",
                  "Myth of sisuphus", "Blade Runner", "wolves of the calla", "mary had a little lamb"]
# # results from keyword title field only
results = pd.DataFrame()
results["query"] = books_to_check
idx_one_col = []
title_one_col = []
idx_all_col =[]
title_all_col=[]


for book in books_to_check:
    idx = search.HelperFunctions.query_to_index(dat, book, ["book_title"])
    title_result = dat.iloc[idx]["book_title"]
    idx_one_col.append(idx)
    title_one_col.append(title_result)
    idx2 = search.HelperFunctions.query_to_index(dat, book, ALL_COL)
    title_result_2 = dat.iloc[idx2]["book_title"]
    idx_all_col.append(idx2)
    title_all_col.append(title_result_2)

results["idx_one_col"] = idx_one_col
results["title_one_col"] = title_one_col
results["idx_all_col"]=idx_all_col
results["title_all_col"] =title_all_col
print(results)





# # results from keyword all fields
# for author in authors_to_check:
#     columns = ["book_title", "genre", "author", "summary"]
#     idx = search.HelperFunctions.query_to_index(dat, author, columns)
#     auth_result = dat.iloc[idx]["author"]
#     print(f"For author {author}, index is {idx} and author is {auth_result}")

