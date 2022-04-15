"""Languages support module
"""
from difflib import SequenceMatcher
from googletrans import Translator
import logging as log
import json
import numpy as np
import requests


from utils import bible as Bible
from utils import constants

translator = Translator()

# Available Languages and Versions in the API
dict_api_version = constants.dict_api_version
dict_api_ver2acr = constants.dict_api_ver2acr
dict_api_acr2ver = constants.dict_api_acr2ver
unique_languages_api = constants.unique_languages_api

# Languages comparison
languages_translation_set = constants.languages_translation_set
lang_ver_transl = constants.lang_ver_transl
lang_transl = constants.lang_transl

# Other constants
Books = constants.BOOKS
Dict_books = constants.DICT_BOOKS
JSON_API_URL = constants.JSON_API_URL
JSON_API_URL_2PART = constants.JSON_API_URL_2PART


def similar(string_1: str, string_2: str) -> float:
    """
    Compares to strings and verify their similarity ratio

    Args:
        string_1 (str):
            String to be compared

        string_2 (str):
            String to be compared

    Return:
        Similarity ratio (float beteween 0.0 - 1.0)
    """
    return SequenceMatcher(None, string_1, string_2).ratio()


def verify_book(book: str, books: list = Books):
    """
    Verify and Identify the book (input) according to the Books list,
    returns the most similar book name.

    Args:
        book (str):
            Input of the user you want to verify

        books (list):
            List of known books (given by default in constants)

    Return:
        The most similar book to the input in the list (str)
    """
    similarity_vec = [similar(book, each) for each in books]
    return books[np.argmax(similarity_vec)]


def verify_book_chapter(book: str, chapter: str, bible_version: str = "akjv"):
    """
    Verify the if the given chapter of a given book exists.

    Args:
        book (str): Given book of the Bible
        chapter (int): Given chapter number
        bible_version (str): Version of the Bible

    Return:
        boolean telling if the chapter exists (True) or no (False)
    """

    try:
        requesting = requests.get(
            (
                (((JSON_API_URL + book) + chapter) + JSON_API_URL_2PART)
                + bible_version
            )
        )

        text = requesting.text[1:-2]
        json.loads(text)  # Only to check if is something there
        return True
    except Exception as exception:
        print(exception)
        return False


def verify_language(
    language_input: str,
    lang_ver_transl: list = list(lang_ver_transl),
    lang_transl: list = list(lang_transl),
) -> str:
    """Function to verify the desired language

    Args:
        language_input (str):
            Desired language.

        lang_ver_transl (list, optional):
            Defaults to list(lang_ver_transl).

        lang_transl (list, optional):
            Defaults to list(lang_transl).

    Returns:
        A string with the suggested language
    """
    languages = lang_transl + lang_ver_transl
    language_input = translator.translate(language_input, dest="english").text
    similarity_vec = [similar(language_input, each) for each in languages]
    return languages[np.argmax(similarity_vec)]


def verify_version(
    version_input: str, versions: list = list(dict_api_ver2acr.keys())
) -> str:
    """Function to verify the bible version.

    Args:
        version_input (str):
            Desired Bible version input.

        versions (list, optional):
            Default list of the available Bible versions.

    Returns:
        A string with the suggested bible version
    """
    similarity_vec = [similar(version_input, each) for each in versions]
    return versions[np.argmax(similarity_vec)]


def translate_message(
    message: str, language: str = "English", src: str = "auto"
):
    """
    Translates a text from an automatic source language to English

    Args:
        message (str):
            Message to translate.

        language (str):
            Objective language

        src (str):
            Source language

    Return:
        Translated text into the goal language
    """
    try:
        if src == "English" and language == "English":
            return message
        else:
            return translator.translate(
                message, dest=language, src=src
            ).text.replace("/ ", "/")
    except (Exception) as exception:
        log.critical(f"In send translated message - Exception: {exception}")
        print("Connection Error")
