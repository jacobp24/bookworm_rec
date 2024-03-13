""" 
UI Module for Bookworm App

FUNCTIONS
========
display_avg_ratings_slider():
    Displays average ratings slider; returns input.

display_num_ratings_slider():
    Displays slider for number of ratings; returns input.

display_search_mode_ui():
    Displays text box for user to enter desired search method; returns input.

display_search_value_ui(search_mode):
    Displays text box for user to enter query to search; retrieves user input.

display_genre_dropdown():
    Displays drop down for genre selection; retrieves value; returns input.

main()
    Displays UI; gathers user feedback; executes serach.
    
"""


import base64
import streamlit as st

# import streamlit.components.v1 as components
try:
    from search_wrapper import search_wrapper
except ImportError:
    from bookworm.search_wrapper import search_wrapper


# Set page configuration
st.set_page_config(
    layout="wide",  # Wide layout to utilize maximum width
    initial_sidebar_state="auto",  # Automatically show/hide the sidebar
    page_title="Book Recommender Tool",  # Title of the page
    page_icon=":books:",  # Icon for the page
    )


# Define CSS for styling
def local_css(file_name):
    """
    Loads a local CSS file to style the Streamlit app.

    This function reads a CSS file, converts it into a string, and then 
    includes it in the Streamlit app using the `st.markdown` function. 
    The CSS string is included in a `<style>` HTML tag and is marked as 
    safe HTML, which allows the CSS to be rendered correctly by the browser.

    Parameters:
    file_name (str): The name of the CSS file to load.

    Raises:
    FileNotFoundError: If the CSS file cannot be found.
    """

    with open(file_name, encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


try:
    local_css("styles.css")  # Load custom CSS
except FileNotFoundError:
    local_css("bookworm/styles.css")


# DEFINE GLOBAL CONSTANTS
SM_DICT = {
    "Title": "Books similar to my favorite book", 
    "Author1": "Books similar to those by my favorite author",
    "Plot": "Books similar to my favorite plot",
    "Genre": "Most popular books in my favorite Genre",
    "Author2": "Most popular books by my favorite author"
}

SEARCH_MODES = [SM_DICT["Title"], SM_DICT["Author1"], SM_DICT["Plot"],
                SM_DICT["Genre"], SM_DICT["Author2"]]
GENRES = [
    "Science Fiction", "Fiction", "Fantasy", "Mystery", "Novel",
    "Children's Literature", "Other", "Historical", "Thriller",
    "Young Adult", "Crime", "Horror", "Romance", "Autobiography/Memoir",
    "Dystopian", "Comedy", "Non-fiction", "Satire", "Biography",
    "History", "Philosophy", "Science"
]


# DEFINE EACH UI ELEMENT AS A SEPARATE FUNCTION
def display_avg_ratings_slider():
    """ 
    Displays average ratings slider, values 0 to 10.  Returns user input.  
    
        Return value
            User's selected average ratings, as a float. 
    """
    return st.slider("Exclude Books with Average Ratings Lower than:",
                     min_value=0.0, max_value=10.0,
                     value=0.0, step=0.5, key="Ave. Ratings Slider",
                     help="Set the minimum average rating.")


def display_num_ratings_slider():
    """ 
    Displays slider for number of ratings; returns user input. 
    
        Return value
            User's selected number of ratings, as an int.  
    
    """
    return st.slider("Exclude Books that have been rated by fewer than:",
                     min_value=0, max_value=50,
                     value=0, step=1, key="Num. Ratings Slider",
                     help="Set the minimum number of ratings.")


def display_search_mode_ui():
    """ 
    Display text box for user to enter desired search method; returns input.
    
        Return value
            User's search mode selection, as a string. 
    """

    help_text_string = "Choose how you want to prioritize your search."
    selection = st.selectbox("Search Mode", [None] + SEARCH_MODES,
                             help=help_text_string, key="search_mode")

    search_mode = ""
    for key, value in SM_DICT.items():
        if value == selection:
            search_mode = key
            break

    return search_mode


def display_search_value_ui(search_mode):
    """ Display text box for user to enter query to search; returns input. 

        Return value
            User's search query, as a string. 
    """

    if search_mode == "Genre":
        return display_genre_dropdown()
    display_str = search_mode
    if display_str in ["Author1", "Author2"]:
        display_str = display_str[:-1]
    return st.text_input(f"Input your favorite {display_str}",
                         key="search_val")


def display_genre_dropdown():
    """ 
    Displays drop down menu for genre selection; returns user input.

        Return value
            User's genre selection as a string. 
    """
    help_text_string = "Select your favorite genre."
    genre_pick = st.selectbox("Favorite Genre", [None] + GENRES,
                              help=help_text_string)
    if genre_pick == "Other":
        return st.text_input("Describe your favorite genre", key="other_genre")
    return genre_pick


def display_search_button(disabled=False):
    """ 
    Displays button to initate search.

        Return value
            Boolean indicating whether user has clicked search.
    """
    return st.button("Search Now", key="search_now",
                     help="Click to initiate search.", type="primary",
                     disabled=disabled, use_container_width=False)


def main():
    """
    Displays UI; gathers user feedback; executes serach.
    """

    # Display header banner with stock image of books
    st.image("images/books_banner.png", use_column_width=True)

    title_image = "images/butterfly.png"

    with open(title_image, "rb") as file:
        image_data = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <div class="container">
            <img class="title-img" src="data:image/png;base64, {image_data}">
            <p class="title-text">The Bookish Butterfly</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add introductory text
    st.write("Welcome to The Bookish Butterfly! A literary guide designed for"
             "bookworms, aiding in the exploration of new books with tailored"
             "preferences. Simply choose how you want to prioritize your"
             "search, input your favorite book, author, plot, or genre. "
             "Adjust the search filters as desired, and click 'Search Now'"
             "to find your next literary adventure.")

    # Display search mode, value, and button
    search_mode = display_search_mode_ui()
    search_val = display_search_value_ui(search_mode)

    # Display filters
    st.write("Adjust search filters as desired:")
    min_ave_rating = display_avg_ratings_slider()
    min_num_ratings = display_num_ratings_slider()

    if search_val not in ["", None]:
        search_button = display_search_button()
        if not search_button:
            st.write("Click 'Search Now' when ready.")
        else:
            with st.spinner('Searching...'):
                try:
                    results = search_wrapper(search_mode, search_val,
                                             min_ave_rating, min_num_ratings)
                    col_to_show = ["book_title", "author", "Book-Rating",
                                   "RatingCount"]
                    st.write(results[col_to_show])
                except ValueError as e:
                    st.write(f"{str(e)}")


main()
