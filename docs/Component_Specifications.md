# Component Specification

## Component #1: User Interface Input
- Displays Interface 
- Collects information from the user: 
  - How does user want to search: Author, Title, Genre, Plotline 
  - What value are they trying to match (Author is x, Title is y, Genre is mystery, Plotline is whatever)
  - How does user want to filter results: star rating, genre, reviewed by however many people  
- Sends information to Search Component  

## Component #2: User Interface Output
- Gets information back from Search component 
- Displays information to user 
- Allow for regeneration of results with different filter values
- [Stretch] Allow user to find book on goodreads/amazon/library or other 

## Component #3: Search/Recommender Engine 
- Orchestration: What type of search to do (will depend on user input): 
  - If genre - simple search for highest rated matching results, filter by user preference
  - Otherwise
    - Use hybrid (keyword + semantic search) 
    - Adjust search weightings based on search modality 
  - Filter results by user preference

![Book Recommendation Flow](/Users/lawrie/Downloads/Bookworm2.png)
