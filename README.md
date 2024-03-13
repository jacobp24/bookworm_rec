# The bookworm project. 
[![build_test](https://github.com/jacobp24/bookworm_rec/actions/workflows/build_test.yml/badge.svg)](https://github.com/jacobp24/bookworm_rec/actions/workflows/build_test.yml)
[![coverage](https://img.shields.io/coverallsCoverage/github/jacobp24/bookworm_rec)](https://github.com/jacobp24/bookworm_rec)


Jacob Peterson, Lawrie Brunswick, Priyam Gupta, Sue Boyd 

##  Project Type
Tool 

## Table of Contents
- [Introduction](#introduction)
- [Questions of Interest](#questions-of-interest)
- [Repository Structure](#repository-structure)
- [Data Sources](#data-sources)
- [Local Setup and Environment](#local-setup-and-environment)
- [Examples](#examples)

## Introduction

With millions of books able to be read, it can be daunting to find the perfect book. Book recommendation tools aim to provide a one stop shop for your next read. Our book recommendation tool, "The Bookish Butterfly" employs a multi-modal approach to offer users a personalized approach. Unlike some recommender systems that only rely on ratings or genres, our model integrates multiple search modalities to provide better recommendations. We provide many options to the user depending on what they are looking for and do the heavy lifting to get some books that will be a great next read. There's no advertising influence here!


## Questions of Interest
### MVP: 
- What book should I read next?
- What other books can I read from the same author?
- Which book would be a good read related to my current book?
- What books have similar plots to a book I liked?
- What are the popular or trending books in a particular genre?


## Repository Structure

[Find it here](docs/project_tree.md)

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

Make sure your current directory is set the 'bookworm_rec' folder. If it is not please run this from within the `bookworm_rec` directory:
```bash
cd bookworm_rec
```

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
1. Make sure your current directory is set the 'bookworm_rec' folder. If it is not please run this from within the `bookworm_rec` directory:
```bash
cd bookworm_rec
```
2. Click [Here](https://dash.voyageai.com/) to create your own API KEY.

3. Copy your new API key and run this command:
```bash
export API_KEY="replace-with-your-api-key"
```
This command is space specific i.e. there cannot be spaces before and after the equals. Make sure your new API KEY
is in double quotes!

4. To check that the API KEY was created successfully:
```bash
echo $API_KEY
```

5. Okay now we are ready to run the application!
```bash
streamlit run app.py
```
Go check out our application in your local browser!!!


## Examples

Here is a [video demonstration](docs/demo_for_3_13.mp4) of our app!

OR

A walkthrough of application can be found in the [examples folder](examples/README.md)



