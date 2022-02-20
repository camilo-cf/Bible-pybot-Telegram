"""
    Unit tests for the Bible class.
"""
import unittest
import random
import string

import sys
sys.path.append('./src/')

from utils import bible
import utils.constants as K

class TestBible(unittest.TestCase):
    def test_similar(self):
        self.assertGreaterEqual(bible.similar('John', 'Jonh'), 0.7)
        self.assertGreaterEqual(bible.similar('John', 'Jhn'), 0.7)
        self.assertGreaterEqual(bible.similar('John', 'Jon'), 0.7)
        self.assertGreaterEqual(bible.similar('John', 'Joh'), 0.7)

    def test_verify_book(self):
        for each in K.BOOKS:
            word = each
            word_list = list(word)
            # Changes 2 random letters in the book name
            for _ in range(1):
                word_list[random.randint(
                    0, len(word_list)-1)] = random.choice(string.ascii_lowercase)
            word = "".join(word_list)
            if each not in ["Kings", "Job", "Peter", "Corinthians", "John", "Acts", "Amos"]:
                self.assertEqual(bible.verify_book(word, K.BOOKS), each)

    def test_verify_book_chapter(self):
        for book, n_chapters in K.TEST_BOOK_CHAPTERS.items():
            self.assertEqual(bible.verify_book_chapter(book, n_chapters), True)

    def test_get_chapter(self):
        self.assertNotEqual(bible.get_chapter('Genesis', 1), None)

    def test_get_message(self):
        self.assertEqual(bible.get_message(
            'Genesis 1:1'), "1 In the beginning God created the heaven and the earth.\r\n")
