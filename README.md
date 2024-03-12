# The bookworm project. 
[![build_test](https://github.com/jacobp24/bookworm_rec/actions/workflows/build_test.yml/badge.svg)](https://github.com/jacobp24/bookworm_rec/actions/workflows/build_test.yml)
[![coverage](https://img.shields.io/coverallsCoverage/github/jacobp24/bookworm_rec)](https://github.com/jacobp24/bookworm_rec)


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
### Book Ratings
[Book Crossing Dataset](https://www.kaggle.com/datasets/ruchi798/bookcrossing-dataset/data)
Includes:
1.  BX-Book-Ratings.csv 
    - 1149779 values
    - Fields: User ID, ISBN, Book Rating
2.  BX-Books.csv 
    - 271379 unique values
    - Fields: ISBN, Book-Title, Book-Author, Year-Of-Publication, Publisher, Image-URL-S, Image-URL-M, Image-URL-L

### Plot Summaries
[Kaggle CMU Book Summary](https://www.kaggle.com/datasets/ymaricar/cmu-book-summary-dataset?resource=download) 
3. BookSummaries.txt
    - 16,559 values
    - Fields: Wikipedia article ID, Freebase ID, Book Title, Author, Publication Date, Book Genres, Plot Summary

### ISBN Matching
[Google Books API](https://developers.google.com/books/)
4. Google Books API
    - ISBN (13 digit)
    - Book Title

## Local Setup and Environment

### Local Setup

This repository can be cloned onto your local computer by running the following command in a terminal:
```bash
$ cp `git clone https://github.com/jacobp24/bookworm_rec.git`
```

If git is not already downloaded, use the [Git Guide](https://github.com/git-guides/install-git) and then clone the repository.

### Environment

For this repository we have set up a environment that can be ran locally and install Python dependicies with
appropriate version requirements. Conda needs to be installed before running the next commands. 
Refer to [Conda Installation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) for further instructions.






