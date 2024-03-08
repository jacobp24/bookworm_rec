import streamlit as st
import numpy as np 
import pandas as pd 
import base64
try:
    from search_wrapper import search_wrapper as search_wrapper
except: 
    from bookworm.search_wrapper import search_wrapper as search_wrapper

# Import Material components for styling
import streamlit.components.v1 as components

# Set page configuration
st.set_page_config(
    layout="wide",  # Wide layout to utilize maximum width
    initial_sidebar_state="auto",  # Automatically show/hide the sidebar
    page_title="Book Recommender Tool",  # Title of the page
    page_icon=":books:",  # Icon for the page
    )

# Define CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("styles.css")  # Load custom CSS


# DEFINE GLOBAL CONSTANTS
SM_DICT = {
    "Title": "Books similar to my favorite book", 
    "Author1": "Books similar to those by my favorite author",
    "Plot": "Books similar to my favorite plot",
    "Genre": "Most popular books in my favorite Genre",
    "Author2": "Most popular books by my favorite author"
}

SEARCH_MODES = [SM_DICT["Title"], SM_DICT["Author1"], SM_DICT["Plot"], SM_DICT["Genre"], SM_DICT["Author2"]]
GENRES = ["Science", "Mystery", "Other"] 

# DEFINE EACH UI ELEMENT AS A SEPARATE FUNCTION 
def display_avg_ratings_slider():
    return st.slider("Exclude Books with Average Ratings Lower than:", min_value=0.0, max_value=10.0, \
                     value=0.0, step=0.5, key="Ave. Ratings Slider", help="Set the minimum average rating.")

def display_num_ratings_slider():
    return st.slider("Exclude Books that have been rated by fewer than:", min_value=0, max_value=50, \
                    value=0, step=1, key="Num. Ratings Slider", help="Set the minimum number of ratings.")
    
def display_search_mode_ui():
    help_text_string = "Choose how you want to prioritize your search." 
    selection = st.selectbox("Search Mode", [None] + SEARCH_MODES, help=help_text_string, key="search_mode")

    search_mode = ""
    for key, value in SM_DICT.items():
        if value == selection:
            search_mode = key
            break

    return search_mode

def display_search_value_ui(search_mode): 
    if search_mode == "Genre": 
        return display_genre_dropdown()
    else:
        display_str = search_mode
        if display_str in ["Author1", "Author2"]:
            display_str = display_str[:-1]
        return st.text_input(f"Input your favorite {display_str}", key="search_val")
   
def display_genre_dropdown():
    help_text_string = "Select your favorite genre." 
    genre_pick = st.selectbox("Favorite Genre", [None] + GENRES, help=help_text_string)
    if genre_pick == "Other":
        return st.text_input("Describe your favorite genre", key="other_genre")
    else: 
        return genre_pick

def display_search_button():
    return st.button("Search Now", key="search_now", help="Click to initiate search.", type="primary", \
                     disabled=False, use_container_width=False)
    
def execute_query(search_mode, search_value, min_ave_rating, min_num_ratings):
    st.write(f"Searching for books using {search_mode}, value: {search_value}, min average rating: {min_ave_rating}, min number of ratings: {min_num_ratings}") 

def main():
    # Display header banner with stock image of books

    st.image("images/books_banner.png", use_column_width=True)

    title_image = "images/butterfly.png"


    st.markdown(
        f"""
        <div class="container">
            <img class="title-img" src="data:image/png;base64,{base64.b64encode(open(TITLE_IMAGE, "rb").read()).decode()}">
            <p class="title-text">The Bookish Butterfly</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    
    # Add introductory text
    st.write("Welcome to The Bookish Butterfly! An literary guide designed for bookworms, aiding in the exploration of new books with tailored preferences. "
             "Simply choose how you want to prioritize your search, input your favorite book, author, plot, or genre. "
             "Adjust the search filters as desired, and click 'Search Now' to find your next literary adventure.")

    # Display search mode, value, and button
    search_mode = display_search_mode_UI()
    search_val = display_search_value_UI(search_mode)
    
    # Display filters
    st.write("Adjust search filters as desired:")
    min_ave_rating = display_avg_ratings_slider()
    min_num_ratings = display_num_ratings_slider()

    search_button = display_search_button()

    if search_val not in ["", None]:
        st.write("Click 'Search Now' when ready.")
        if search_button:
            results = search_wrapper(search_mode, search_val, min_ave_rating, min_num_ratings)
            col_to_show = ["book_title", "author", "Book-Rating", "RatingCount"]
            st.write(results[col_to_show])

main()
