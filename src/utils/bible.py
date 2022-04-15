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


def get_chapter(book: str, chapter: int, bible_version: str = "akjv"):
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
    requesting = requests.get(
        (
            ((JSON_API_URL + book) + str(chapter) + JSON_API_URL_2PART)
            + bible_version
        )
    )
    return requesting.text[1:-2]


def get_message(message: str, bible_version: str = "akjv"):
    """Get the passage of the Bible given an income message.

    Args:
        message (str):
            An input text that should be something like
            "John 14:6" or "Exodus 17:1-6" or "Genesis 1".

        bible_version (str):
            Version of the Bible.

    Return:
        The message of the bible in the given book and chapter (str) [it can be long].
    """
    book = validations.verify_book(message)
    details = message.split(" ")[-1]
    message = " ".join([book, details]).replace(".", "")

    if message[-1].isnumeric():
        requesting = requests.get(
            JSON_API_URL + message + JSON_API_URL_2PART + bible_version
        )
        try:
            text = requesting.text[1:-2]
            jsontxt = json.loads(text)

            try:
                verses = list(jsontxt["book"][0]["chapter"].keys())
                full_verses = [
                    str(each_verse)
                    + " "
                    + jsontxt["book"][0]["chapter"][each_verse]["verse"]
                    for each_verse in verses
                ]

            except Exception:
                verses = list(jsontxt["chapter"].keys())
                full_verses = [
                    f"{str(each_verse)} "
                    + jsontxt["chapter"][each_verse]["verse"]
                    for each_verse in verses
                ]

            if text == "U":
                full_verses = "Error - Passage not found"
        except Exception:
            full_verses = "Error"
    else:
        full_verses = "Error - Verify the chapter of the passage"

    return "".join(full_verses)


def get_next_chapter(present_chapter: str, bible_version: str = "akjv"):
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
    book = validations.verify_book(present_chapter)
    chapter = present_chapter.split(" ")[-1].replace(".", "")
    present_chapter = " ".join([book, chapter])

    try:
        new_chapter = int(chapter) + 1
        next_chapter = " ".join([book, str(new_chapter)])
        requesting = requests.get(
            JSON_API_URL + next_chapter + JSON_API_URL_2PART + bible_version
        )

        text = requesting.text[1:-2]

        if text == "U":
            number_book = Dict_books[book]
            new_book = Books[number_book + 1 - 1]
            new_chapter = 1
            next_chapter = " ".join([new_book, str(new_chapter)])

    except Exception:
        number_book = 0
        new_book = Books[number_book + 1 - 1]
        new_chapter = 1
        next_chapter = " ".join([new_book, str(new_chapter)])
    return next_chapter
