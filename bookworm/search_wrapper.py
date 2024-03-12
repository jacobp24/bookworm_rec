
""" 
Module to orchestrate search based on user inputs. 

Assembles data to search over; calls proper search function given user 
preferred search mode; and filters results based on user filters.

FUNCTIONS
=========

assemble_data(path1, path2, path3, path4)
    Assembles data split into 4 pieces wtih same column names
    
filter_ratings(results, min_ave_ratings, min_num_rating)
    Filters serach results by user ratings prefrences. 

select_search(search_mode, search_value, min_ave_rating, 
                  min_num_ratings, num_book=10)
    Selects and implements search based on user search mode.

search_wrapper(search_mode, search_value, min_ave_rating, 
                   min_num_ratings, num_books=10)
    Searches and filters book databse based on given inputs. 
    
"""

try:
    import search
except ImportError:
    # pylint: disable=consider-using-from-import
    import bookworm.search as search
import pandas as pd

def assemble_data(path1, path2, path3, path4):
    """ 
    Function to assemble data split into 4 pieces wtih same column names.
    Paramaters:
        Path_X: The file path name.  Must be a valid path and a csv file.
                Assumes only the first path has column headers.
    Returns: 
        An assembled dataframe.
    """

    # Read the first dataframe, which will provide the column names
    df1 = pd.read_csv(path1)
    # Read the remaining dataframes without adding headers
    df2 = pd.read_csv(path2)
    df3 = pd.read_csv(path3)
    df4 = pd.read_csv(path4)
    df2.columns = df1.columns
    df3.columns = df1.columns
    df4.columns = df1.columns
    df = pd.concat([df1, df2, df3, df4], ignore_index=True)
    return df

def assemble_embeddings_data():
    """
    Functions that assembles the data with embeddings
    """
    # Create file paths

    path_root = "data/complete_w_embeddings/complete_w_embeddings.csv"
    path1 = path_root + "_part_1.csv"
    path2 = path_root + "_part_2.csv"
    path3 = path_root + "_part_3.csv"
    path4 = path_root + "_part_4.csv"
    return assemble_data(path1, path2, path3, path4)

# Filter
def filter_ratings(results, min_ave_ratings, min_num_rating):

    """ 
    Filters search results by user ratings prefrences. 

    Filter by min ave ratings if min_ave_ratigns > 0.0, otherwise 
    keeps all, including "none" values. Likewise filters by 
    min_num_ratings if min_num_ratings > 0. 
    
    Paramaters
        Results: The search results to be filterd. Must be a df with 
            columns "Book-Ratings" and "Rating Count".
        min_ave_ratings:  A float. The min ave ratings to filter
        min-num_ratings: An int.  The min number of ratings to filter on.
    Returns: 
        A dataframe of filtered results
    """

    if not "Book-Rating" in results.columns:
        raise ValueError("Your data must have a Book-Ratings column")
    if not "RatingCount" in results.columns:
        raise ValueError("Your data must have a RatingCount column")

    if min_ave_ratings != 0.0:
        subset_df = results[results['Book-Rating'] > min_ave_ratings]
    else:
        subset_df = results
    if min_num_rating != 0:
        results_filtered = subset_df[subset_df['RatingCount'] > min_num_rating]
    else:
        results_filtered = subset_df
    return results_filtered

def select_search(search_mode, search_value, num_books=10):
    """
    Selects and implements search based on user search mode.

    Parameters:
        search_mode: str
            The mode of search ('Author2', 'Title', 'Plot', 'Genre').
        search_value: str
            The value to search for.
        num_books: int, optional
            The number of books to return from the search, pre-filtering.

    Returns:
        pandas.DataFrame
            A dataframe of search results.
    """
    if search_mode == "Author1":

        df_r = pd.read_csv("data/complete_w_ratings.csv")
        results1 = search.author2_search(df_r, search_value,
                                        num_books=max(num_books * 2, 20))

        df_e = assemble_embeddings_data()
        results2 = search.semantic_search(df_e, search_value, ["author"],
                                         num_books=max(num_books * 2, 20))

       # Concatenate the dataframes by alternating rows
        combined_df = pd.DataFrame()
        for i in range(max(len(results1), len(results2))):
            if i < results1.shape[0]:
                combined_df = pd.concat([combined_df, results1.iloc[[i]]])
            if i < results2.shape[0]:
                combined_df = pd.concat([combined_df, results2.iloc[[i]]])
        combined_df.reset_index(drop=True, inplace=True)
        results = combined_df

    elif search_mode == "Title":
        df = assemble_embeddings_data()
        results = search.semantic_search(df, search_value, ["book_title"],
                                         num_books=max(num_books * 2, 20))
    elif search_mode == "Plot":
        df = assemble_embeddings_data()
        results = search.plot_semantic_search(df, search_value,
                                              num_books=max(num_books * 2, 20))
    elif search_mode == "Author2":
        df = pd.read_csv("data/complete_w_ratings.csv")
        results = search.author2_search(df, search_value,
                                        num_books=max(num_books * 2, 20))

    else: #search_mode == "Genre"
        try:
            genre_df = pd.read_csv("bookworm/data/genre.csv")
        except FileNotFoundError:
            genre_df = pd.read_csv("data/genre.csv")
        results = search.genre_search(genre_df, search_value,
                                      num_books=max(num_books * 2, 20))

    return results

def search_wrapper(search_mode, search_value, min_ave_rating,
                   min_num_ratings, num_books=10):
    """
    Searches and filters based on given inputs. 

    Assembles data to search over; calls proper search function given user 
    preferred search mode; and filters results based on user filters.

    Paramaters
        Search_mode: A string. 
        Search_value: A string. 
        min_ave_ratings: A float. The min ave ratings to filter
        min-num_ratings: An int.  The min number of ratings to filter on.
        num_books: # of books returned from the search, pre-filtering.
    Returns
        A dataframe of filtered search results. 
    """

    # search
    results = select_search(search_mode, search_value, num_books)

    #filter
    results_filtered = filter_ratings(results, min_ave_rating, min_num_ratings)
    return results_filtered.head(num_books)
