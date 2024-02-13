
# UI Layer for Book Recommender Tool 

# Import Needed Libraries 
import streamlit as st
import numpy as np 
import pandas as pd 



# DEFINE GLOBAL CONSTANTS 

# Dictionary of possible seach modes and explanatory text
SM_DICT = {
    "Title": "Books similar to my favorite book", 
    "Author1": "Books similar to those by my favorite author",
    "Plot": "Books similar to my favorite plot",
    "Genre": "Most popular books in my favorite Genre",
    "Author2": "Most popular books by my favorite author"
}

SEARCH_MODES = [SM_DICT["Title"], SM_DICT["Author1"], SM_DICT["Plot"], SM_DICT["Genre"], SM_DICT["Author2"]]
GENRES = ["Science", "Mystery", "Other"] # TO DO - INPUT ACTUAL LIST OF GENRES FROM DATA 



# DEFINE EACH UI ELEMENT AS A SEPARATE FUNCTION 

# Define display_search_mode_UI
# A function that display a drop down menu of search modes
# That corresponds to values in the SM_DICT
# and returns the Key in SM_DICT that corresponds to that value 
def  display_search_mode_UI():
    help_text_string = "explanations . .  " # TO DO: insert actual helptext
    selection = st.selectbox( "How do you want to prioritize your search",  \
                               [None] + SEARCH_MODES, help = help_text_string)
    
    # The user selection is a value in SM_DICT
    # Iterate over SM_DICT to find the relevant key
    search_mode = ""
    for key, value in SM_DICT.items():
        if value == selection:
            search_mode = key
            break

    return search_mode


# Define function to display genre_choices
# If Search Mode is "Genres"
def display_genre_dropdown():
    help_text_string = "explanations . .  " # TO DO: insert actual helptext
    genre_pick = st.selectbox( "What is your favorite Genre?",  \
                               [None] + GENRES, help = help_text_string)
    if genre_pick == "Other":
        return(st.text_input(f"Describe your favorite genre", key="other_genre"))
    else: 
        return(genre_pick)

# Define display_search_value_UI
# a function that gets users input of what to search on
# Takes as input the search mode 
def display_search_value_UI(search_mode): 
    

    # for genre only, display drop down choices 
    if search_mode == "Genre": 
        return(display_genre_dropdown())


    else: # everything else gets a simple free form text box   
        display_str = search_mode
        
        # Remove final char from Author1, Author2 as needed
        if display_str in ["Author1", "Author2"]:
            display_str = display_str[:-1]
    
        return st.text_input(f"Input your favorite {display_str}", key="search_val")
   
    

# Define display_ratings_slider
# A function to allow user to request filtering 
# Results by average ratings 
def display_avg_ratings_slider():
    return(st.slider("Exclude Books with Average Ratings Lower than:", min_value=0.0, max_value=5.0, \
                     value=3.0, step=0.5, key="Ave. Ratings Slider", help="help text here")) 
# TO DO: add actual help text
# TO DO: Confirm min and max average ratings available 
    
# Define display_num_ratings_slider
# A function to allow user to request filtering 
# By minimum number of reviewers 
def display_num_ratings_slider():
    return(st.slider("Exclude Books that have been rated by fewer than:", min_value=0, max_value=50, \
                     value=25, step=1, key="Num. Ratings Slider", help="help text here")) 
# TO DO: add actual help text
# TO DO: Confirm appropriate min/max points for slider 



# Define a function that display the search now button
# Returns true if button clicked, otherwise false

def display_search_button():
    return(st.button("Search Now", key="search_now", help="help_text", type="primary", \
                     disabled=False, use_container_width=False))
    


# Define execute_query 
# a function that invokes the query layer
def execute_query(search_mode, search_value, min_ave_rating, min_num_ratings):
    # TO DO:  Update code to call the execute search model 
    # For now, as placeholder, just print out parameteres we are searching over    
    st.write(f"Ok, we will search for books using seach mode is {search_mode} \
             and search value is {search_value} \
             and min average ratings is {min_ave_rating} \
             and min number of ratings is {min_num_ratings}") 





# MAIN Function to orchestrate UI 
def main():
    search_mode = display_search_mode_UI()
    if search_mode:
        search_val = display_search_value_UI(search_mode)
        if not (search_val in ["", None]):
            st.write("Please adjust search filters as desired and click Search Now when ready")
            min_ave_rating = display_avg_ratings_slider()
            min_num_ratings = display_num_ratings_slider()
            if display_search_button():
                execute_query(search_mode, search_val, min_ave_rating, min_num_ratings)
    


main()



