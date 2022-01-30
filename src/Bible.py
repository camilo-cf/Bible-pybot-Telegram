import requests
import json
from googletrans import Translator
from difflib import SequenceMatcher
import numpy as np

########################################################################
######################         Constants          ###################### 
########################################################################

Books=['Genesis','Exodus','Leviticus','Numbers','Deuteronomy','Joshua',
           'Judges','Ruth','1Samuel','2Samuel','1Kings','2Kings','1Chronicles',
           '2Chronicles','Ezra','Nehemiah','Esther','Job','Psalms','Proverbs',
           'Ecclesiastes','SongofSolomon','Isaiah','Jeremiah','Lamentations',
           'Ezekiel','Daniel','Hosea','Joel','Amos','Obadiah','Jonah','Micah',
           'Nahum','Habakkuk','Zephaniah','Haggai','Zechariah','Malachi',
           'Matthew','Mark','Luke','John','Acts','Romans','1Corinthians',
           '2Corinthians','Galatians','Ephesians','Philippians','Colossians',
           '1Thessalonians','2Thessalonians','1Timothy','2Timothy','Titus',
           'Philemon','Hebrews','James','1Peter','2Peter','1John','2John',
           '3John','Jude','Revelation']

Dict_books = dict(zip(Books, range(1,len(Books)+1)))

json_api_url = "https://getbible.net/json?passage="
json_api_url_2part = "&version="

#Constructor of the translator
translator = Translator()

########################################################################



########################################################################
######################         Functions          ###################### 
########################################################################

def similar(a, b):
    '''
    Compares to strings and verify their similarity ratio

    Args:
        a (str): String to be compared
        b (str): String to be compared

    Return:
        similarity ratio (float betweenn 0.0 - 1.0)
    '''
    return SequenceMatcher(None, a, b).ratio()


def verify_book(book, books=Books):
    '''
    Verify and Identify the book (input) according to the Books list, returns the most similar book name

    Args:
        book (str): Input of the user you want to verify
        books (list): List of known books (given by default in constants)
    
    Return:
        The most similar book to the input in the list (str)
    '''
    similarity_vec=[]

    for each in books:
        similarity_vec.append(similar(book,each))

    return books[np.argmax(similarity_vec)]


def verify_book_chapter(book, chapter, bible_version = 'akjv'):
    '''
    Verify the if the given chapter of a given book exists

    Args:
        book (str): Given book of the Bible
        chapter (int): Given chapter number
        bible_version (str): Version of the Bible

    Return:
        boolean telling if the chapter exists (True) or no (False)
    '''

    try:
        requesting = requests.get(json_api_url+str(book)+str(chapter)+json_api_url_2part+bible_version)
        text = requesting.text[1:-2]
        json.loads(text) # Only to check if is something there
        return True
    except:
        return False


def get_chapter(book, chapter, bible_version = 'akjv'):   
    '''
    Gey the Bible chapter

    Args:
        book (str): Given book of the Bible
        chapter (int): Given chapter number
        bible_version (str): Version of the Bible

    Return:
        The message of the bible in the given book and chapter (str) [it can be long]
    '''
    requesting = requests.get(json_api_url+str(book)+str(chapter)+json_api_url_2part+bible_version)
    return requesting.text[1:-2]

def get_message(message, bible_version = 'akjv'):
    '''
    Get the passage of the Bible given an income message 

    Args:
        message (str): An input text that should be something like "John 14:6" or "Exodus 17:1-6" or "Genesis 1"
        bible_version (str): Version of the Bible

    Return:
    The message of the bible in the given book and chapter (str) [it can be long]
    '''
    book = verify_book(message)
    details = message.split(" ")[-1]
    message = " ".join([book,details])

    if message[-1].isnumeric():
        requesting = requests.get(json_api_url+str(message)+json_api_url_2part+bible_version)
        text = requesting.text[1:-2]
        jsontxt = json.loads(text)

        try:
            verses = list(jsontxt['book'][0]['chapter'].keys())
            full_verses = []
            for each_verse in verses:    
                full_verses.append((str(each_verse)+" "+ jsontxt['book'][0]['chapter'][each_verse]['verse']))

        except:
            verses = list(jsontxt['chapter'].keys())
            full_verses = []
            for each_verse in verses:    
                full_verses.append((str(each_verse)+" "+ jsontxt['chapter'][each_verse]['verse']))

        if text=='U':
            full_verses="Error - Passage not found"
    else:
        full_verses="Verify the chapter of the passage"


    final_message = "".join(full_verses)
    return(final_message)
    

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

def get_next_chapter(present_chapter, bible_version = 'akjv'):    
    '''
    Returns the next chapter in a given book and chapter 

    Args:
        present_chapter (str): String with a book of theb bible and chapter, for example "John 1"
        bible_version (str): Version of the Bible

    Returns:
        text describing the next book and chapter
        
    Example:
        get_next_chapter('John 1')
        > John 2

    '''
    book = verify_book(present_chapter)
    chapter = present_chapter.split(" ")[-1]
    present_chapter = " ".join([book,chapter])

    try:
        new_chapter=int(chapter)+1
        next_chapter = " ".join([book,str(new_chapter)])
        requesting = requests.get(json_api_url+str(next_chapter)+json_api_url_2part+bible_version)
        text = requesting.text[1:-2]

        if text == 'U':
            n = Dict_books[book]
            new_book = Books[n+1-1]
            new_chapter = 1
            next_chapter = " ".join([new_book,str(new_chapter)])
            
    except:
        n = 0# starting over again
        new_book = Books[n+1-1]
        new_chapter = 1
        next_chapter = " ".join([new_book,str(new_chapter)])

    return next_chapter


