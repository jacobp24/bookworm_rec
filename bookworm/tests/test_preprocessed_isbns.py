"""
This module contains a class of test cases for testing the functions
in the preprocessed_isbns module.

Purpose: Tests the validity of the transform_isbn, check_digit_13,
convert_10_to_13 and complete_to_13 functions.

Usage: Uses the unittest framework, run by the command:
    python -m unittest discover OR
    by running the following command from the bookworm folder:
    python -m bookworm.tests.test_preprocessed_isbns
"""

import unittest

try:
    from preprocessed_isbns import transform_isbn, check_digit_13, \
                                   convert_10_to_13, complete_to_13
except ImportError:
    from bookworm.preprocessed_isbns import transform_isbn, check_digit_13, \
                                            convert_10_to_13, complete_to_13


class TestTransformISBN(unittest.TestCase):
    """
    Class of tests for the transform_isbn function in preproccesed_isbns.py.
    Provides one shot tests and edge cases for the function.
    Employs the unittest framework.

    Arguments: Unittest Framework
    Returns: Either all passing tests or indicates test failures.
    """

    def test_transform_isbn_13(self):
        """
        One shot test for testing if the function provides
        a simple cut of the last 2 '.0' from the isbn.
        """
        result = transform_isbn("9788831000154.0")
        self.assertEqual(result, "9788831000154")

    def test_transform_isbn_10(self):
        """
        One shot test for doing nothing if ISBN is already 10 digits.
        """
        result = transform_isbn("1234567890")
        self.assertEqual(result, "1234567890")

    def test_transform_invalid_isbn(self):
        """
        Test that function returns None with an invalid value.
        """
        result = transform_isbn("123456.9")
        self.assertIsNone(result)

    def test_isbn_is_str(self):
        """
        Test that anything other than a string returns a ValueError.
        """
        with self.assertRaises(ValueError):
            transform_isbn(98)


class TestCheckDigit13(unittest.TestCase):
    """
    Class of tests for the check_digit_13 function in preproccesed_isbns.py.
    Provides a smoke test, one shot tests and edge cases for the function.
    Employs the unittest framework.

    Arguments: Unittest Framework
    Returns: Either all passing tests or indicates test failures.
    """

    def test_smoke(self):
        """
        Tests that function does not release the magical smoke when called.
        """
        result = check_digit_13("978883100015")
        assert result is not None

    def test_must_be_12(self):
        """
        Tests that function raises an appropriate value error if ISBN is not
        12 digits long.
        """
        with self.assertRaises(ValueError):
            check_digit_13("12345")
            check_digit_13("1000000000000000000000")

    def test_must_be_str(self):
        """
        Tests that function raises an appropriate value error is ISBN is not
        a string.
        """
        with self.assertRaises(ValueError):
            check_digit_13(888888888888)
            check_digit_13(8888888888.0)

    def test_one_shot(self):
        """
        One shot test for ensuring the generated 13th digit
        is created correctly.
        """

        result = check_digit_13("978883100015")
        self.assertEqual(result, "4")

        result2 = check_digit_13("978043942010")
        self.assertEqual(result2, "5")

    def test_generated_0(self):
        """
        Tests edge case of the generated value if it is 0.
        """

        result = check_digit_13("978853253079")
        self.assertEqual(result, "0")


class TestConvert13(unittest.TestCase):
    """
    Class of tests for the convert_10_to_13 function in preproccesed_isbns.py.
    Provides one shot tests and edge cases for the function.
    Employs the unittest framework.

    Arguments: Unittest Framework
    Returns: Either all passing tests or indicates test failures.
    """

    def test_smoke(self):
        """
        Tests that function does not release the magical smoke when called.
        """
        result = convert_10_to_13("8831000158")
        assert result is not None

    def test_valid_isbn_10(self):
        """
        One shot test for returning the correct conversion from
        ISBN-10 to ISBN-13.
        """
        isbn_10 = "0123456789"
        result = convert_10_to_13(isbn_10)
        expected_result = "9780123456786"
        self.assertEqual(result, expected_result)

        isbn_10 = "8831000152"
        result = convert_10_to_13(isbn_10)
        expected_result = "9788831000154"
        self.assertEqual(result, expected_result)

    def test_invalid_isbn_len(self):
        """
        Tests that function return value error if the isbn argument
        is not of length 10.
        """
        isbn_short = "123456789"
        with self.assertRaises(ValueError):
            convert_10_to_13(isbn_short)

        isbn_long = "12345678901"
        with self.assertRaises(ValueError):
            convert_10_to_13(isbn_long)

    def test_edge_case_empty_isbn(self):
        """
        Tests that an empty string raises a ValueError.
        """

        isbn_empty = ""
        with self.assertRaises(ValueError):
            convert_10_to_13(isbn_empty)


class TestComplete13(unittest.TestCase):
    """
    Class of tests for the complete_to_13 function in preproccesed_isbns.py.
    Provides one shot tests and edge cases for the function.
    Employs the unittest framework.

    Arguments: Unittest Framework
    Returns: Either all passing tests or indicates test failures.
    """

    def test_valid_isbn_10(self):
        """
        Tests that an ISBN-10 is converted to 13 properly.
        """

        isbn_10 = "0123456789"
        result = complete_to_13(isbn_10)
        expected_result = "9780123456786"
        self.assertEqual(result, expected_result)

    def test_valid_isbn_13(self):
        """
        Tests that an ISBN-13 stays unchanged.
        """

        isbn_13 = "9780123456785"
        result = complete_to_13(isbn_13)
        self.assertEqual(result, isbn_13)

    def test_invalid_isbn_length(self):
        """
        Tests that an ISBN not of length 10 or 13 raises a value error.
        """

        isbn_short = "123456789"
        with self.assertRaises(ValueError):
            complete_to_13(isbn_short)

        isbn_long = "12345678901234"
        with self.assertRaises(ValueError):
            complete_to_13(isbn_long)

    def test_edge_case_empty_isbn(self):
        """
        Tests that a empty string returns a value error.
        """

        isbn_empty = ""
        with self.assertRaises(ValueError):
            complete_to_13(isbn_empty)

    def test_non_string_input(self):
        """
        Tests that a non-string input raises a value error.
        """
        non_string_input = 12345
        with self.assertRaises(ValueError):
            complete_to_13(non_string_input)


if __name__ == "__main__":
    unittest.main()
