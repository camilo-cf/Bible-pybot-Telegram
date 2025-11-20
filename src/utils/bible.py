"""
    Library of Bible functions
"""
import json
import requests

import utils.validations as validations
import utils.constants as constants

# Constants
Books = constants.BOOKS
Dict_books = constants.DICT_BOOKS
JSON_API_URL = constants.JSON_API_URL
JSON_API_URL_2PART = constants.JSON_API_URL_2PART


def get_chapter(book: str, chapter: int, bible_version: str = "akjv") -> str:
    """Get the Bible chapter

    Args:
        book (str):
            Given book of the Bible

        chapter (int):
            Given chapter number

        bible_version (str):
            Version of the Bible

    Return:
        The message of the bible in the given book and chapter (str) [it can be long]
    """
    try:
        # v2 API format: https://query.getbible.net/v2/{version}/{book} {chapter}
        url = f"{JSON_API_URL}{bible_version}/{book}%20{chapter}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # v2 API returns dict with key like "akjv_1_1"
        if data:
            first_key = list(data.keys())[0]
            chapter_data = data[first_key]
            verses = chapter_data.get('verses', [])
            return json.dumps(chapter_data)  # Return as JSON string
        return "Error: No data"
    except Exception as e:
        return f"Error: {str(e)}"


def get_message(message: str, bible_version: str = "akjv") -> list:
    """Get the passage of the Bible given an income message.

    Args:
        message (str):
            An input text that should be something like
            "John 14:6" or "Exodus 17:1-6" or "Genesis 1".

        bible_version (str):
            Version of the Bible.

    Return:
        A list with the message of the bible in the given book and chapter (list) [it can be long].
    """
    try:
        book = validations.verify_book(message)
        details = message.split(" ")[-1]
        passage = " ".join([book, details]).replace(".", "")

        if not passage[-1].isnumeric():
            return ["Error - Verify the chapter of the passage"]

        # v2 API format: https://query.getbible.net/v2/{version}/{book} {chapter}:{verse}
        url = f"{JSON_API_URL}{bible_version}/{passage.replace(' ', '%20')}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return ["Error - Passage not found"]
        
        data = response.json()
        
        if not data:
            return ["Error - Passage not found"]
        
        # v2 API returns dict with key like "akjv_43_3" 
        first_key = list(data.keys())[0]
        chapter_data = data[first_key]
        verses = chapter_data.get('verses', [])
        
        if not verses:
            return ["Error - No verses found"]
        
        # Format verses as "verse_number verse_text"
        full_verses = [
            f"{v['verse']} {v['text'].strip()}"
            for v in verses
        ]
        
        return ["".join(full_verses)]
        
    except Exception as e:
        return [f"Error: {str(e)}"]


def get_next_chapter(present_chapter: str, bible_version: str = "akjv") -> str:
    """Returns the next chapter in a given book and chapter

    Args:
        present_chapter (str):
            String with a book of the bible and chapter, for example "John 1"

        bible_version (str):
            Version of the Bible

    Returns:
        text describing the next book and chapter

    Example:
        get_next_chapter('John 1')
        > John 2

    """
    try:
        book = validations.verify_book(present_chapter)
        chapter = present_chapter.split(" ")[-1].replace(".", "")
        present_chapter = " ".join([book, chapter])

        # Try next chapter
        next_chapter = " ".join([book, str(int(chapter) + 1)])
        url = f"{JSON_API_URL}{bible_version}/{next_chapter.replace(' ', '%20')}"
        response = requests.get(url, timeout=10)
        
        # If chapter exists, return it
        if response.status_code == 200:
            data = response.json()
            if data:  # Chapter exists
                return next_chapter
        
        # Chapter doesn't exist, move to next book
        number_book = Dict_books.get(book, 0)
        if number_book < len(Books):
            new_book = Books[number_book]  # Next book (already +1 due to 1-indexing)
            new_chapter = 1
            return " ".join([new_book, str(new_chapter)])
        else:
            # Reached end, start over
            return "Genesis 1"
            
    except Exception:
        return "Genesis 1"
