"""
Script to create embeddings for test data
"""


import pandas as pd
import nltk
#from nltk.tokenize import word_tokenize
import voyageai


nltk.download('punkt')

df = pd.read_csv("bookworm/data/test_data.csv")
vo = voyageai.Client(api_key="pa-rhN-u_ArM1uxKF78V1JeB8-TJZM0lQlA60SIavXNHbg")

def token_count(summary):
    """ 
    Function to count token in given parameter summary; returns int.
    """
    return vo.count_tokens([summary])

# Apply the token_count function to each summary and filter rows
df['token_count'] = df['summary'].apply(token_count)
filtered_df = df[df['token_count'] <= 4000]

# Drop the token_count column as it's no longer needed
filtered_df = filtered_df.drop(columns=['token_count'])

# Convert your dataframe summaries column to a list and prepare them
texts = filtered_df['summary'].tolist()

# get embeddings
embeddings = vo.embed(texts, model="voyage-lite-02-instruct",
                      input_type="document").embeddings

# add embeddings to data frame
filtered_df["embeddings"] = embeddings

# save to CSV
filtered_df.to_csv("bookworm/data/test_data_w_embeddings.csv")
