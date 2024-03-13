# Needed to do this for the use of a general exception to deal with broad API errors.
# pylint: disable=W0718,W0621,E0401,C0103
"""
This script processes a dataset of book summaries to generate and utilize embeddings
for semantic analysis, leveraging the voyageai API for embedding generation.
"""

# Import third-party libraries
import pandas as pd
import nltk
from voyageai import Client as VoyageClient

# Download the 'punkt' tokenizer model
nltk.download('punkt')

# Load the dataset
DATA_PATH = "complete_w_ratings.csv"
df = pd.read_csv(DATA_PATH)

# Initialize the voyageai Client
voyage_client = VoyageClient(api_key="")

def token_count(summary, client):
    """
    Counts the number of tokens in a summary using the voyageai Client.

    Parameters:
    - summary: The text summary to count tokens in.
    - client: The voyageai client instance.

    Returns:
    - The token count.
    """
    return client.count_tokens([summary])

# Apply token counting
df['token_count'] = df['summary'].apply(lambda x: token_count(x, voyage_client))
filtered_df = df[df['token_count'] <= 4000]
filtered_df.drop(columns=['token_count'], inplace=True)

# Prepare texts for embedding generation
text_summaries = filtered_df['summary'].tolist()

def generate_embeddings(texts, client, batch_size=24):
    """
    Generates embeddings for a list of texts in batches.

    Parameters:
    - texts: A list of text summaries.
    - client: The voyageai client instance.
    - batch_size: The size of each batch for processing.

    Returns:
    - A list of embeddings.
    """
    all_embeddings = []
    progress_count = 0

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        try:
            batch_result = client.embed(batch_texts, model="voyage-lite-02-instruct",
                                        input_type="document")
            batch_embeddings = batch_result.embeddings
            all_embeddings.extend(batch_embeddings)
        except Exception:  # Use of a general exception to deal with broad API Errors.
            process_individual_texts(batch_texts, all_embeddings, client)

        # Progress update
        progress = (progress_count / (len(texts) / batch_size)) * 100
        print(f"\rProgress: {progress:.2f}%", end='')
        progress_count += 1

    print("\nDone!")
    return all_embeddings

def process_individual_texts(batch_texts, embeddings, client):
    """
    Process each text in a batch individually if the batch process fails.

    Parameters:
    - batch_texts: The batch of texts to process.
    - embeddings: The list to append embeddings to.
    - client: The voyageai client instance.
    """
    for text in batch_texts:
        try:
            result = client.embed([text], model="voyage-lite-02-instruct",
                                  input_type="document")
            embeddings.extend(result.embeddings)
        except Exception:  # Use of a general exception to deal with broad API Errors
            embeddings.append(None)

# Generate embeddings
embeddings = generate_embeddings(text_summaries, voyage_client)
filtered_df["embeddings"] = embeddings

# Save the processed dataframe
OUTPUT_PATH = "complete_w_embeddings.csv"
filtered_df.to_csv(OUTPUT_PATH)

print(f"DataFrame shape: {filtered_df.shape}")
