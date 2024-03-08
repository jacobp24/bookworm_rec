# %%
import os
import pandas as pd
import numpy as np

import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

import voyageai

# %%
import time

# %%
df = pd.read_csv("C:/Users/stlp/Desktop/Geeky/Software/bookworm_local/attempt_1/complete_w_ratings.csv")

# %%
df.columns

# %% [markdown]
# # Generating Embeddings

# %% [markdown]
# After refrencing MTEB leaderboard on huggingface and reading a lot, alot of documentation. The best embedding model for our use case is voyage-elite-instruct. Since it is the highest ranked model in STS(Semantic Textual Similairity) which is our exact use case. Since we need to value semantic understanding more for our task.

# %%
vo = voyageai.Client(api_key="pa-rhN-u_ArM1uxKF78V1JeB8-TJZM0lQlA60SIavXNHbg")

# %%
df.columns

# %% [markdown]
# ## A data cleaning step for convenience that can be optimized later

# %%
def token_count(summary):
    return vo.count_tokens([summary])

# %%
# Apply the token_count function to each summary and filter rows
df['token_count'] = df['summary'].apply(token_count)
filtered_df = df[df['token_count'] <= 4000]

# %%
# Drop the token_count column as it's no longer needed
filtered_df = filtered_df.drop(columns=['token_count'])

# %% [markdown]
# ## back to the task at hand

# %%
# Convert your dataframe summaries column to a list and prepare them
texts = filtered_df['summary'].tolist()

# %%
# sanity check
count = 0
for i in range(len(texts)):
    if len(texts[i]) > 4000:
        count += 1
count

# %%
df.columns

# %%
s = word_tokenize(df["summary"][12])
len(s)

# %%
len(df["summary"][12])

# %%
total_tokens = vo.count_tokens([df["summary"][12]])
print(total_tokens)

# %%
# sanity check
count = 0
for i in range(len(texts)):
    total_tokens = vo.count_tokens([texts[i]])
    if total_tokens > 4000:
        count += 1
count

# %% [markdown]
# ## back to embeddings

# %%
# Recommended batch size from documentation and embeddings initialization
batch_size = 24

# %%
embeddings = []
progress_count = 0

# Process texts in batches
for i in range(0, len(texts), batch_size):
    batch_texts = texts[i:i + batch_size]
    try:
        # First attempt: Request embeddings for the entire batch
        batch_embeddings = vo.embed(batch_texts, model="voyage-lite-02-instruct", input_type="document").embeddings
        embeddings.extend(batch_embeddings)
    except:
        # If the batch request fails, process each text individually
        batch_embeddings = []
        for text in batch_texts:
            try:
                # Request embedding for the current text individually
                embedding = vo.embed([text], model="voyage-lite-02-instruct", input_type="document").embeddings
                batch_embeddings.extend(embedding)
            except:
                # Append None for this text if an individual request also fails
                batch_embeddings.append(None)
        # Extend the embeddings list with results (successful or None for failures)
        embeddings.extend(batch_embeddings)

    # Optional: Wait for 0.1 seconds before proceeding to the next batch
    # time.sleep(0.1)

    # Progress update
    progress = (progress_count / (len(texts) / batch_size)) * 100
    print(f"\rProgress: {progress:.3f}%", end='')
    progress_count += 1

print("\nDone!")


# %%
filtered_df["embeddings"] = embeddings

# %%
filtered_df.to_csv("complete_w_embeddings.csv")

# %%
filtered_df.shape

# %% [markdown]
# # Chunking

# %%
import pandas as pd
import numpy as np

# %%
df = pd.read_csv("C:/Users/stlp/Desktop/Geeky/Software/bookworm_local/attempt_1/complete_w_embeddings.csv")

# %%
import os

def split_csv_into_chunks(filename, chunk_count=4):
    # Step 1: Calculate the total number of lines in the original file
    with open(filename, 'r', encoding='utf-8') as file:
        total_lines = sum(1 for line in file)
    
    # Calculate the number of lines per chunk, excluding the header if present
    lines_per_chunk = total_lines // chunk_count
    extra_lines = total_lines % chunk_count

    # Step 2: Split the file
    with open(filename, 'r', encoding='utf-8') as file:
        for chunk in range(chunk_count):
            # Determine the filename for the chunk
            chunk_filename = f'{filename}_part_{chunk + 1}.csv'
            
            # Write a portion of lines to the new chunk file
            with open(chunk_filename, 'w', encoding='utf-8') as chunk_file:
                for _ in range(lines_per_chunk + (1 if chunk < extra_lines else 0)):
                    line = file.readline()
                    # This check helps to avoid writing empty lines at the end
                    if not line:
                        break
                    chunk_file.write(line)
            print(f'Chunk {chunk + 1} written to {chunk_filename}')

# Example usage
split_csv_into_chunks('C:/Users/stlp/Desktop/Geeky/Software/bookworm_local/attempt_1/complete_w_embeddings.csv')


# %%



