"""
    Library of Bible functions
"""
from difflib import SequenceMatcher
import json
from googletrans import Translator
import numpy as np
import requests

import utils.constants as constants

########################################################################
######################         Constants          ######################
########################################################################
Books = constants.BOOKS
Dict_books = constants.DICT_BOOKS
JSON_API_URL = constants.JSON_API_URL
JSON_API_URL_2PART = constants.JSON_API_URL_2PART
########################################################################


########################################################################
######################         Functions          ######################
########################################################################
# Constructor of the translator
translator = Translator()

def similar(string_1, string_2):
    '''
    Compares to strings and verify their similarity ratio

    Args:
        string_1 (str): String to be compared
        string_2 (str): String to be compared

    Return:
        similarity ratio (float betweenn 0.0 - 1.0)
    '''
    return SequenceMatcher(None, string_1, string_2).ratio()


def verify_book(book, books=Books):
    '''
    Verify and Identify the book (input) according to the Books list,
    returns the most similar book name.

    Args:
        book (str): Input of the user you want to verify
        books (list): List of known books (given by default in constants)

    Return:
        The most similar book to the input in the list (str)
    '''
    similarity_vec = []
    for each in books:
        similarity_vec.append(similar(book, each))
    return books[np.argmax(similarity_vec)]


def verify_book_chapter(book, chapter, bible_version='akjv'):
    '''
    Verify the if the given chapter of a given book exists.

    Args:
        book (str): Given book of the Bible
        chapter (int): Given chapter number
        bible_version (str): Version of the Bible

    Return:
        boolean telling if the chapter exists (True) or no (False)
    '''

    try:
        requesting = requests.get(
            JSON_API_URL+str(book)+str(chapter)+JSON_API_URL_2PART+bible_version)
        text = requesting.text[1:-2]
        json.loads(text)  # Only to check if is something there
        return True
    except (Exception) as exception:
        print(exception)
        return False


def get_chapter(book, chapter, bible_version='akjv'):
    '''
    Gey the Bible chapter

    Args:
        book (str): Given book of the Bible
        chapter (int): Given chapter number
        bible_version (str): Version of the Bible

    Return:
        The message of the bible in the given book and chapter (str) [it can be long]
    '''
    requesting = requests.get(
        JSON_API_URL+str(book)+str(chapter)+JSON_API_URL_2PART+bible_version)
    return requesting.text[1:-2]


def get_message(message, bible_version='akjv'):
    '''
    Get the passage of the Bible given an income message.

    Args:
        message (str):  An input text that should be something like
                        "John 14:6" or "Exodus 17:1-6" or "Genesis 1".
        bible_version (str): Version of the Bible.

    Return:
        The message of the bible in the given book and chapter (str) [it can be long].
    '''
    book = verify_book(message)
    details = message.split(" ")[-1]
    message = " ".join([book, details])

    if message[-1].isnumeric():
        requesting = requests.get(
            JSON_API_URL+str(message)+JSON_API_URL_2PART+bible_version)
        text = requesting.text[1:-2]
        jsontxt = json.loads(text)

        try:
            verses = list(jsontxt["book"][0]["chapter"].keys())
            full_verses = [
                str(each_verse)
                + " "
                + jsontxt['book'][0]['chapter'][each_verse]['verse']
                for each_verse in verses
            ]

        except Exception as exception:
            print(exception)
            verses = list(jsontxt['chapter'].keys())
            full_verses = [
                str(each_verse) + ' ' + jsontxt['chapter'][each_verse]['verse']
                for each_verse in verses
            ]

        if text == 'U':
            full_verses = "Error - Passage not found"
    else:
        full_verses = "Verify the chapter of the passage"

    return "".join(full_verses)


def translate_message(text, language="English", src='auto'):
    '''
    Translates a text from an automatic source language to English

    Args:
        text (str): text to be translated
        language (str): objective language
        src (str): source language

    Return:
        Translated text into the goal language
    '''
    return translator.translate(text, dest=language, src=src).text


def get_next_chapter(present_chapter, bible_version='akjv'):
    '''
    Returns the next chapter in a given book and chapter

    Args:
        present_chapter (str): String with a book of the bible and chapter, for example "John 1"
        bible_version (str): Version of the Bible

    Returns:
        text describing the next book and chapter

    Example:
        get_next_chapter('John 1')
        > John 2

    '''
    book = verify_book(present_chapter)
    chapter = present_chapter.split(" ")[-1]
    present_chapter = " ".join([book, chapter])

    try:
        new_chapter = int(chapter)+1
        next_chapter = " ".join([book, str(new_chapter)])
        requesting = requests.get(
            JSON_API_URL+str(next_chapter)+JSON_API_URL_2PART+bible_version)
        text = requesting.text[1:-2]

        if text == 'U':
            number_book = Dict_books[book]
            new_book = Books[number_book+1-1]
            new_chapter = 1
            next_chapter = " ".join([new_book, str(new_chapter)])

    except (Exception) as exception:
        print(exception)
        number_book = 0  # starting over again
        new_book = Books[number_book+1-1]
        new_chapter = 1
        next_chapter = " ".join([new_book, str(new_chapter)])

    return next_chapter
