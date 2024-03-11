""" Script to prep text for tokenization

Script takes the data complete_w_ratings.csv and preprocesses the text
fields in preparation for vectorization.

Module should be run from /scripts folder.


"""
import ast
import pandas as pd

def parse_genres(genre_str):
    """ 
    Parse genre dictionaries into keywords joined by commas
        
    Paramters:
         Genres: A dictinonary of genres.
    Return
        A string with genres expressed as keywords, separated
        by commas.  
    """

    try:
        genres_dict = ast.literal_eval(genre_str)
        genres_text = ', '.join(genres_dict.values())
    except (ValueError, SyntaxError):
        genres_text = 'Unknown Genre'
    return genres_text


  
def fill_na(df):
    """ 
    Fill in missing values in dataframe

    Paramaters
        df: A dataframe with fields author, book_title, genre
            and summary. 
    Return: 
        A dataframe with missing values filled in. 
    """

    df.fillna({'author': 'Unknown', 'book_title': 'Unknown',
                'genre': 'Unknown', 'summary': 'No Summary Available'},
                inplace=True)
    return df

   
def preprocess_text(text):
    """
    Convert text to all lowercase.
        
    Parameters:
        Text: A string
    Returns
        A lower case string
    """
    text = str(text).lower()
    return text

def prep_df(df): 

    """"Prepares dataframe for tokenization.
    
    Paramaters:
        df: A dataframe with columns author, book_title, genre, and summary
    Returns:
        Preprocessed dataframe.  Text all losercase and missing values filled.
    """

    df = fill_na(df)
    df["genre"] = df['genre'].apply(parse_genres)
    columns = ["author", "book_title", "genre", "summary"]
    for col in columns: 
        df[col] = df[col].apply(preprocess_text)
    return(df)

#f = "../bookworm/data/test_data/test_data.csv"
f = "../bookworm/data/complete_w_ratings.csv"
dat = pd.read_csv(f)
processed_dat = prep_df(dat)
f = "../bookworm/data/complete_w_ratings_preproc.csv"
processed_dat.to_csv(f)
