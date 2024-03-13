# Component Specification

## Component #1: User Interface 
- Displays Interface 
- Collects information from the user: 
  - How does user want to search: Author_Similar, Author_Favorite, Title, Plot, Genre
  - What value are they trying to match (Author is x, Title is y, Genre is mystery, Plotline is whatever)
  - How does user want to filter results: star rating, genre, reviewed by however many people  
- Sends information to Search Wrapper
- Receives information back from Search Wrapper and displays results 

## Component #2: Search Wrapper
- Receives user input from User Interface 
- Selects appropriate functions(s) and dataset(s) to use given user input
- Retrieves data from Preprocessed Data Layer 
-   If applicable, dynamically assembles and completes any further data preprocessing needed. 
- Calls appropriate search function(s) from Search/Recommender Engine, passing data to use.
- Retrieves results from Search /Recommender Engine 
- If applicable: combines results from different search modes into consolidated
  results (Used in Author_Similar search)
- Fiters books based on user filters as needed
- Passes filtered results back to User Interface 

## Component #3 Search/Recommender Engine 
- Executes search function on data as specified by Search Wrapper 
- Types of search:  
  - Semantic search - Hybird keyword (TfidfVectorizer) match to given field (author/title)
    to impute book under search, choose next closest books via precomputed semantic (Voyeageai) 
    embeddings.
    - Called by Search Wrapper when user selected search mode is Author_similar or Title. 
    - Executed on data: "complete_w_embeddings", passed by Search_Wrapper. 
    - Also loads indices_np, and distances_np from preprocessed data layer. 
  - Plot_Semantic Search - Pure semantic search based on voyageai. 
    - Called by Search Wrapper when user selected search mode is Plot.  
    - Executed on data '"complete_w_embeddings."
  - Author2 Search - Fuzzy matching to author field. 
    - Called by when user selected search mode is Author_Similar or Author_Favorite.
    - Executed on data "complete_w_ratings."
  - Genre search - exact matching to standardized genre field.  
    - Called by Search Wrapper when user selected search mode is Genre.
    - Executed on data "Genre.csv"

## Component #4 Preprocessed Data Layer 

Please see [Here](../bookworm/data/README.md) for a more detailed description of the preprocessed data. 

# <ins>Book Recommendation Flow:</ins>
![image](https://github.com/jacobp24/bookworm_rec/assets/85261391/bf25c3f2-7eab-47ae-b91d-8b2b9482fe5f)


