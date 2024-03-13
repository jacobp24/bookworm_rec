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
- Selects appropriate search modality and database to use given user input
- Calls appropriate function from Search/Recommender Engine 
- Retrieves results from Search /Recommender Engine 
- Gets information back from Search component (up to 20 recommended books)
- Fiters books based on user filters as needed
- Passes filtered results back to User Interface 

## Component #3 Search/Recommender Engine 
- Executes search function on data as specified by Search Wrapper 
- Types of search:  
     (1) Semantic search - hybird keyword (TfidfVectorizer) and
        semantic (Voyeageai) search. Used for Author1 and Book_Title 
        search. Executed on data: "complete_w_embeddings"
    (2) Plot_semantic search based on voyageai semantic search.  Executed on 
    data '"complete_w_embeddings."
    (3) Author2 search - fuzzy matching to author field Executed on data "complete_w_ratings."
    (4) genre search - exact matching to standardized genre field.  Executed on data "Genre.csv"

## Component #4 Preprocessed Dat Layer 
Please see [Here](../bookworm/data/README.md) for a discription of the preprocessed data. 

### <ins>Book Recommendation Flow:</ins>
![Image](https://github.com/jacobp24/bookworm_rec/assets/85261391/8409d54d-e8bc-4b4b-a6e5-ded6c12e8d8d "Book Recommendation Flow")
