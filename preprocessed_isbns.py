""" This module preprocesses book rating and overall book data by
transforming ISBNs and merging ratings. Filters, cleans and formats
ISBN and ratings.


"""


# !/usr/bin/env python
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt


complete = pd.read_csv('data/complete_data.csv')

complete['ISBN'] = complete['ISBN'].astype(str)


def transform_isbn(isbn):
    """ Checks if ISBN is length 13 and cuts off '.0' from float ISBN,
    otherwise just return 10.

    Arguments:
        ISBN as float/int

    Returns:
        ISBN-13 or ISBN-10
    """

    if len(isbn) == 15:
        return isbn[:-2]  # Cut the last two characters
    if len(isbn) == 10:
        return isbn  # No modification needed for 10-digit ISBN
    return None


# Apply the function to the 'ISBN' column
complete['ISBN'] = complete['ISBN'].apply(transform_isbn)

string_length_counts = complete['ISBN'].str.len().value_counts()
complete = complete.dropna(subset=['ISBN'])
# Filtering out rows with invalid ISBNs
filt_complete = complete[complete['ISBN'].str[:-1].str.isnumeric()]

BOOK_RATINGS_PATH = 'data/BX-Book-Ratings.csv'
book_rating = pd.read_csv(BOOK_RATINGS_PATH, sep=';', quotechar='"',
                          encoding='windows-1252')
book_rating['ISBN'] = book_rating['ISBN'].astype(str)
string_length_counts_2 = book_rating['ISBN'].str.len().value_counts()

preprocessed = pd.read_csv('data/Preprocessed_data.csv')
preprocessed['isbn'] = preprocessed['isbn'].astype(str)
preprocessed.rename(columns={'isbn': 'ISBN'}, inplace=True)
string_length_counts_3 = preprocessed['ISBN'].str.len().value_counts()


def check_digit_13(isbn):
    """ Checks that ISBN is currently 12 digits, then uses mathematical
    formula for generation of last digit according to ISBN-13
    standards during conversion.

    Argument:
        ISBN passed in through convert_10_to_13 function
    Exceptions:
        Gives ValueError if ISBN length is not 12 digits.
    Returns:
        Generated digit as a string
    """
    assert len(isbn) == 12
    sum1 = 0
    for i, digit in enumerate(isbn):
        int_c = int(digit)
        num = 3 if i % 2 else 1
        sum1 += num * int_c

    generated = 10 - (sum1 % 10)
    if generated == 10:
        return '0'
    return str(generated)


def convert_10_to_13(isbn):
    """ Checks that passed in ISBN is ISBN-10, then uses ISBN conventions
    for converting ISBN-10 to ISBN-13. Calls check_digit_function for 13th
    number in ISBN generation.

    Argument:
        ISBN passed in through complete_to_13 function
    Exceptions:
        Gives ValueError if ISBN length is not 10 digits.
    Returns:
        Newly created ISBN 13
    """
    assert len(isbn) == 10
    prefix = '978' + isbn[:-1]
    check = check_digit_13(prefix)
    return prefix + check


# Complete changing to all ISBN 13
def complete_to_13(isbn):
    """ Checks if ISBN is ISBN-10 format then calls
    convert_10_to_13 function for conversion.

    Argument:
        ISBN in ISBN-10 or ISBN-13 form

    Returns:
        ISBN-13
    """
    if len(isbn) == 10:
        return convert_10_to_13(isbn)
    return isbn


# Change ISBN from 10 to 13 or keep at 13
filt_complete['isbn_13'] = filt_complete['ISBN'].apply(complete_to_13)

book_rating = book_rating[book_rating['ISBN'].str.len() == 10]

# Filtering out rows with invalid ISBNs
filt_book_rating = book_rating[book_rating['ISBN'].str[:-1].str.isnumeric()]


# Converting from ISBN 10 to ISBN 13
filt_book_rating['isbn_13'] = filt_book_rating['ISBN'].apply(convert_10_to_13)
filt_book_rating.tail()

# Filtering out 0 ratings
filt_book_rating = filt_book_rating[filt_book_rating['Book-Rating'] != 0]

# Counting how many times an ISBN has been rated
rating_counts = filt_book_rating.groupby('isbn_13')['Book-Rating'].count() \
                                .reset_index()
rating_counts.columns = ['isbn_13', 'RatingCount']

# Calculating average ratings
average_ratings = filt_book_rating.groupby('isbn_13')['Book-Rating'].mean() \
                                    .reset_index()

# joining ratings
merged_rating_df = pd.merge(filt_complete, average_ratings, on='isbn_13',
                            how='left')

# joining ratings count
full_merged_df = pd.merge(merged_rating_df, rating_counts, on='isbn_13',
                          how='left')

non_nan_count = full_merged_df['Book-Rating'].count()

plt.hist(full_merged_df['Book-Rating'], bins=20)
plt.title('Book Rating Distribution')
plt.show()

plt.hist(full_merged_df['RatingCount'], bins=20)
plt.title('Rating Count Distribution')
plt.show()

non_nan_rating_count = full_merged_df['RatingCount'].count()

max_rating_count = full_merged_df['RatingCount'].max()

min_rating_count = full_merged_df['RatingCount'].min()

max_rating = full_merged_df['Book-Rating'].max()

min_rating = full_merged_df['Book-Rating'].min()

# Creating cleaned data CSV
full_merged_df.to_csv('complete_w_ratings.csv')


# MAY DELETE LATER DEPENDING ON EMBEDDINGS
# embedded = pd.read_csv('attempt_1/data_with_embeddings.csv')

# updated_embeddings = pd.merge(embedded, full_merged_df, how='inner', \
# on='ISBN')
# updated_embeddings= updated_embeddings.loc[:,~updated_embeddings.columns \
# .duplicated()]
# columns_to_drop = [col for col in updated_embeddings.columns
#                   if col.endswith('_y')]
# updated_embeddings = updated_embeddings.drop(columns=columns_to_drop)
# Remove "_x" from column names
# updated_embeddings.columns = updated_embeddings.columns.str.replace('_x', '')
# updated_embeddings.head()

# updated_embeddings.to_csv('data_w_embeddings_updated.csv')
