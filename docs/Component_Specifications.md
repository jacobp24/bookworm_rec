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
- Calls appropriate search function(s) from Search/Recommender Engine 
- Retrieves results from Search /Recommender Engine 
- If applicable: combines results from different search modes into consolidated
  results (Used in Author_Similar search)
- Fiters books based on user filters as needed
- Passes filtered results back to User Interface 

## Component #3 Search/Recommender Engine 
- Executes search function on data as specified by Search Wrapper 
- Types of search:  
  - Semantic search - hybird keyword (TfidfVectorizer) and
        semantic (Voyeageai) search. Used for Author1 and Book_Title 
        search. Executed on data: "complete_w_embeddings"
  - Plot_semantic search based on voyageai semantic search.  Executed on 
    data '"complete_w_embeddings."
  - Author2 search - Fuzzy matching to author field. Executed on data "complete_w_ratings."
  - Genre search - exact matching to standardized genre field.  Executed on data "Genre.csv"

## Component #4 Preprocessed Dat Layer 

Please see [Here](../bookworm/data/README.md) for a more detailed description of the preprocessed data. 

### <ins>Book Recommendation Flow:</ins>
![Image](https://github.com/jacobp24/bookworm_rec/assets/85261391/8409d54d-e8bc-4b4b-a6e5-ded6c12e8d8d "Book Recommendation Flow")
