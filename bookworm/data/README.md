## This folder contains the data used to run and test the bookworm app. 


# Data Used When Searching by Author Match 
1.  File: ./complete_w_ratings.csv
    - 13639 books (rows)
    - Fields: "book_id", "book_title", "author", "publication_date", "genre",
      "summary", "ISBN13, "Book-Rating", "Rating-Count"
    - This file is the result of running the script preprocessed_isbns.py
    - Note: complete_w_ratings.csv is a subset of the "complete_w_embeddings" 
        dataset, but for perfromance reasons we use this file, rather than 
        the more resource intensive "complete_w_embeddings" file when embeddings
        are not required. 

# Data Used When Performing Semantic Search or Keyword + Semantic Search
2.  Folder: ./complete_w_embeddings
    - Contains the data from "complete_w_ratings.csv" augmented by semantic 
        embeddings as described in the script: ../../scripts/Embeddings.py
    - Due to space limitations, data is chunked into four files and dynamically
        reassembled when needed: 
            ./complete_w_embeddings.csv_part_1.csv
            ./complete_w_embeddings.csv_part_2.csv
            ./complete_w_embeddings.csv_part_3.csv
            ./complete_w_embeddings.csv_part_4.csv
3.  File ./distances_updated.npy
    - For each book, semantic distances to the next closest 21 books, based on 
        semantic distances computed via Voyeate API
    - Output of script ../../scripts/Semantic Scores.py
4.  Filed ./indices_updated.npy
    - For each book, indices of the top 21 closest books, based on semantic 
        distances computed via Voyeage API
    - Output of script ../../scripts/Semantic Scores.py

# Data Used When Performing Genre Field Match

5.  File ./genre.csv
    - 26347 rows
        - A single book can appear in multiple rows if multiple generic_genre
          classificatinos.  
    - Fields: "book_id", "book_title", "author", "publication_date", "genre",
      "summary", "ISBN13, "Book-Rating", "Rating-Count", "generic_genre"



# Test Data in Folder test_data
Test analogues to above files.  Generally same/similar datasets as described 
above on a samller scale, for purposes of testing.  
