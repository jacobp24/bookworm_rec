# The bookworm project. 
[![build_test](https://github.com/jacobp24/bookworm_rec/actions/workflows/build_test.yml/badge.svg)](https://github.com/jacobp24/bookworm_rec/actions/workflows/build_test.yml)


Jacob Peterson, Lawrie Brunswick, Priyam Gupta, Sue Boyd 

##  Project Type
Tool 

## Questions of Interest
### MVP: 
- What book should I read next?
- What other books can I read from the same author?
- Which book would be a good read related to my current book?
- What books have similar plots to a book I liked?
- What are the popular or trending books in a particular genre?
- What books have people who share my interests rated highly? 

### Time permitting (stretch)
 - Where can I buy that book or is it available?
 - Are there new releases or popular books that match my tastes?
 - Can I find hidden gems or underrated books that match my tastes?

## Goal for Project Output 
- We will create a simple UI for users to receive recommendations for books that they might like to read. 
Users can input variables such as: previous book(s) that they have enjoyed, authors, titles, years, and/or similar plots, and the tool will make selections for other books they may wish to read. (Exact parameters tbd; part of our project will be to explore the optimal model and parameters for our rating system). 
- (Stretch) The tool will also provide a link to purchasing the book on Amazon or other venues. 

## Data Sources 
### We will definitely use
[Book Crossing Dataset](https://www.kaggle.com/datasets/ruchi798/bookcrossing-dataset/data)
Includes:
1.  BX-Book-Ratings.csv 
    - 1149779 values
    - Fields: User ID, ISBN, Book Rating
2.  BX-Books.csv 
    - 271379 unique values
    - Fields: ISBN, Book-Title, Book-Author, Year-Of-Publication, Publisher, Image-URL-S, Image-URL-M, Image-URL-L

### We may also use 
1.  [Seattle Library Collection Inventory](https://www.kaggle.com/datasets/ymaricar/cmu-book-summary-dataset/code)
    - Fields: Title, author, ISBN, item count, location
2. [Goodreads-books](https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks)
    - Fields: Book ID (ISBN), title, authors, number of ratings, average rating 
3. [Another Bookcrossing Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)
4.  Amazon API (TBD)
5.  Google Shopping (TBD)

