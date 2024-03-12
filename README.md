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
    - A copy of this data is in [data_raw/BX-Book_Ratings.csv](data_raw/BX-Book-Ratings.csv)
2.  BX-Books.csv 
    - 271379 unique values
    - Fields: ISBN, Book-Title, Book-Author, Year-Of-Publication, Publisher, Image-URL-S, Image-URL-M, Image-URL-Lnot
    - Due to file size, this file was **not** included in the repo, but can be obtained from the link above.  

### Plot Summaries
[Kaggle CMU Book Summary](https://www.kaggle.com/datasets/ymaricar/cmu-book-summary-dataset?resource=download) 

3. BookSummaries.txt
    - 16,559 values
    - Fields: Wikipedia article ID, Freebase ID, Book Title, Author, Publication Date, Book Genres, Plot Summary
    - The data from BookSummaries.txt was extracted into the file [data_raw/complete_data.csv](data_raw/complete_data.csv)

### ISBN Matching
[Google Books API](https://developers.google.com/books/)

4. Google Books API
    - ISBN (13 digit)
    - Book Title
    - This API was used to augment CMU data with ISBN Numbers to help for matching with Book Ratings dataset
    - ISBN numbers obtained via Google APIs also included in [data_raw/complete_data.csv](data_raw/complete_data.csv)
  
A description of data cleaning, joining and preprocessing can be found [Here](bookworm/data/Data_Processing_Slides.pdf)

## Local Setup and Environment

### Local Setup

This repository can be cloned onto your local computer by running the following command in a terminal:
```bash
git clone https://github.com/jacobp24/bookworm_rec.git
```

If git is not already downloaded, use the [Git Guide](https://github.com/git-guides/install-git) and then clone the repository.

### Environment

For this repository we have set up a environment that can be ran locally and install Python dependencies with
appropriate version requirements. Conda needs to be installed before running the next commands. 
Refer to [Conda Installation](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) for further instructions.

Now run the next command to create the `bookworm_env` Conda environment:

```bash
conda env create -f env.yml
```
Make sure to activate the newly created environment:
```bash
conda activate bookworm_env
```
Once done with the environment (after using the tool), deactivate it by running:
```bash
conda deactivate
```

### Application

Our application runs with the Streamlit Python library. Before jumping onto the webpage,
you will need to do the following steps:

In order to generate the recommendation embeddings we utilized the [VoyageAI](https://www.voyageai.com/) package.

Please create a local API KEY by following these steps:

1. Click [Here](https://dash.voyageai.com/) to create your own API KEY.

2. Copy your new API key and run this command:
```bash
export API_KEY="replace-with-your-api-key"
```
This command is space specific i.e. there cannot be spaces before and after the equals. Make sure your new API KEY
is in double quotes!

3. To check that the API KEY was created successfully:
```bash
echo $API_KEY
```

4. Make sure your current directory is set the 'bookworm' folder. If it is not please run this from within the `bookworm_rec` directory:
```bash
cd bookworm
```

5. Okay now we are ready to run the application!
```bash
streamlit run app.py
```
Go check out our application in your local browser!!!


### Examples

Here is a [video demonstration]() of our app!

OR

A walkthrough of application can be found in the [examples folder](examples/README.md)



