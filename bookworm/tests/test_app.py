"""
Module: test_app

This module contains unit tests for the Streamlit UI functions implemented in
the 'app.py' module. The unit tests cover the functionality of various UI
elements and ensure that they behave as expected.

The tests are organized into a TestCase class named TestStreamlitUI, where
each test method corresponds to a specific UI function.

Test Cases:
- Test the main function by mocking the search_wrapper function and verifying
    its behavior.
- Test each UI element function individually by patching Streamlit functions
    and asserting their output.

Dependencies:
- unittest: The built-in unit testing framework in Python.
- patch: A utility from the unittest.mock module used for mocking objects
    during testing.
- pandas: A library for data manipulation and analysis.

Usage:
Run this module to execute the unit tests for the Streamlit UI functions.

"""

import unittest
from unittest.mock import patch

import pandas as pd


from app import main, display_avg_ratings_slider, display_num_ratings_slider, \
                display_search_mode_ui, display_search_value_ui, \
                display_genre_dropdown, display_search_button, execute_query


class TestStreamlitUI(unittest.TestCase):
    """Test cases for the Streamlit UI functions."""

    def setUp(self):
        """Set up test environment."""
        self.mock_image_data = b'fake image data'
        self.mock_image_path = 'books_banner.png'

    @patch('search_wrapper.search_wrapper')
    def test_main(self, mock_search_wrapper):
        """Test the main function."""
        # Mock data
        mock_search_wrapper.return_value = pd.DataFrame({
            'Book-Rating': [8.0, 7.5, 6.0, 9.0, 8.5]  # Example data
        })

        # Call the main function
        main()

    def test_display_avg_ratings_slider(self):
        """Test display_avg_ratings_slider function."""
        with patch('streamlit.slider') as mock_slider:
            mock_slider.return_value = 5.0
            result = display_avg_ratings_slider()
            self.assertEqual(result, 5.0)

    def test_display_num_ratings_slider(self):
        """Test display_num_ratings_slider function."""
        with patch('streamlit.slider') as mock_slider:
            mock_slider.return_value = 10
            result = display_num_ratings_slider()
            self.assertEqual(result, 10)

    def test_display_search_mode_ui(self):
        """Test display_search_mode_ui function."""
        with patch('streamlit.selectbox') as mock_selectbox:
            mock_selectbox.return_value = "Books similar to my favorite book"
            result = display_search_mode_ui()
            self.assertEqual(result, "Title")

    def test_display_search_value_ui(self):
        """Test display_search_value_ui function."""
        with patch('streamlit.text_input') as mock_text_input:
            mock_text_input.return_value = "The Great Gatsby"
            result = display_search_value_ui("Title")
            self.assertEqual(result, "The Great Gatsby")

    def test_display_genre_dropdown(self):
        """Test display_genre_dropdown function."""
        with patch('streamlit.selectbox') as mock_selectbox, \
                patch('streamlit.text_input') as mock_text_input:
            mock_selectbox.return_value = "Science"
            result = display_genre_dropdown()
            self.assertEqual(result, "Science")

            mock_selectbox.return_value = "Other"
            mock_text_input.return_value = "Space Opera"
            result = display_genre_dropdown()
            self.assertEqual(result, "Space Opera")

    def test_display_search_button(self):
        """Test display_search_button function."""
        with patch('streamlit.button') as mock_button:
            mock_button.return_value = True
            result = display_search_button()
            self.assertTrue(result)

    def test_execute_query(self):
        """Test execute_query function."""
        with patch('streamlit.write') as mock_write:
            execute_query("Title", "The Great Gatsby", 8.0, 20)
            mock_write.assert_called_once_with(
                """Searching for books using Title, value: The Great Gatsby,
                    min average rating: 8.0, min number of ratings: 20""")


if __name__ == '__main__':
    unittest.main()
