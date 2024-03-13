# Book Summary Embeddings and Nearest Neighbors Analysis

This repository contains Python scripts for generating embeddings from book summaries using the voyageai API and performing nearest neighbors analysis on the generated embeddings. The project aims to semantically analyze book summaries to find similarities and recommend books based on content.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6+
- pandas
- numpy
- scikit-learn
- nltk
- A valid API key from voyageai

## Configuration

1. Obtain an API key from [voyageai](https://voyageai.com/). You will need to sign up for an account and subscribe to a plan that suits your needs.
2. Once you have your API key, open `embeddings.py` and locate the following line:

    ```python
    client = voyageai.Client(api_key="")
    ```

3. Replace the empty string with your API key:

    ```python
    client = voyageai.Client(api_key="YOUR_API_KEY_HERE")
    ```

## Files Description

- `Embeddings.py`: This script processes a dataset of book summaries to generate embeddings using the voyageai API. It includes data cleaning, token counting, and embedding generation.

- `Semantic Scores.py`: After generating embeddings, this script loads them and uses the k-Nearest Neighbors algorithm to find and analyze the closest summaries based on their semantic similarity.

## Running the Scripts

1. Place your dataset in the same directory as the scripts or update the file paths in the scripts to where your dataset is located.

2. Run `embeddings.py` first to generate embeddings for your dataset. This will create a new CSV file with the embeddings included.

    ```bash
    python embeddings.py
    ```

3. After generating the embeddings, run `Semantic Scores.py` to perform the nearest neighbors analysis.

    ```bash
    python nearest_neighbors.py
    ```