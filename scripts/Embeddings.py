"""
This script processes a dataset of book summaries to generate and utilize embeddings
for semantic analysis, leveraging the voyageai API for embedding generation.
"""

# Import standard libraries
import os
import time

# Import third-party libraries
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
import voyageai

# Download the 'punkt' tokenizer model
nltk.download('punkt')

# Load the dataset
DATA_PATH = "C:/Users/stlp/Desktop/Geeky/Software/bookworm_local/attempt_1/complete_w_ratings.csv"
df = pd.read_csv(DATA_PATH)

# Load the instance of the model
client = voyageai.Client(api_key="")

def token_count(summary):
    """
    Counts the number of tokens in a summary using the voyageai Client.

    Parameters:
    - summary: The text summary to count tokens in.

    Returns:
    - The token count.
    """
    return client.count_tokens([summary])

# Data cleaning and preprocessing
df['token_count'] = df['summary'].apply(token_count)
filtered_df = df[df['token_count'] <= 4000]
filtered_df.drop(columns=['token_count'], inplace=True)

# Prepare texts for embedding generation
texts = filtered_df['summary'].tolist()

def generate_embeddings(texts, batch_size=24):
    """
    Generates embeddings for a list of texts in batches.

    Parameters:
    - texts: A list of text summaries.
    - batch_size: The size of each batch for processing.

    Returns:
    - A list of embeddings.
    """
    client = voyageai.Client(api_key="")
    embeddings = []
    progress_count = 0

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        try:
            batch_embeddings = client.embed(batch_texts, model="voyage-lite-02-instruct", input_type="document").embeddings
            embeddings.extend(batch_embeddings)
        except Exception:
            process_individual_texts(batch_texts, embeddings, client)

        # Progress update
        progress = (progress_count / (len(texts) / batch_size)) * 100
        print(f"\rProgress: {progress:.3f}%", end='')
        progress_count += 1

    print("\nDone!")
    return embeddings

def process_individual_texts(batch_texts, embeddings, client):
    """
    Process each text in a batch individually if the batch process fails.

    Parameters:
    - batch_texts: The batch of texts to process.
    - embeddings: The list to append embeddings to.
    - client: The voyageai client instance.
    """
    batch_embeddings = []
    for text in batch_texts:
        try:
            embedding = client.embed([text], model="voyage-lite-02-instruct", input_type="document").embeddings
            batch_embeddings.extend(embedding)
        except Exception:
            batch_embeddings.append(None)
    embeddings.extend(batch_embeddings)

# Generate embeddings
embeddings = generate_embeddings(texts)
filtered_df["embeddings"] = embeddings

# Save the processed dataframe
OUTPUT_PATH = "complete_w_embeddings.csv"
filtered_df.to_csv(OUTPUT_PATH)

print(f"DataFrame shape: {filtered_df.shape}")
