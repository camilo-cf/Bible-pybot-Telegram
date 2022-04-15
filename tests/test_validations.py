"""
    Unit tests for the Bible class.
"""
import unittest
import random
import sys
import string

sys.path.append("./src/")
import utils.constants as K
import utils.validations as validations


class TestValidations(unittest.TestCase):
    def test_similar(self):
        self.assertGreaterEqual(validations.similar("John", "Jonh"), 0.7)
        self.assertGreaterEqual(validations.similar("John", "Jhn"), 0.7)
        self.assertGreaterEqual(validations.similar("John", "Jon"), 0.7)
        self.assertGreaterEqual(validations.similar("John", "Joh"), 0.7)

    def test_verify_book(self):
        for each in K.BOOKS:
            word = each
            word_list = list(word)
            # Changes 2 random letters in the book name
            for _ in range(1):
                word_list[
                    random.randint(0, len(word_list) - 1)
                ] = random.choice(string.ascii_lowercase)
            word = "".join(word_list)
            if each not in [
                "1Kings",
                "2Kings",
                "Job",
                "Joel",
                "1Peter",
                "2Peter",
                "3Peter",
                "1Corinthians",
                "2Corinthians",
                "John",
                "1John",
                "2John",
                "3John",
                "Acts",
                "Amos",
                "1Samuel",
                "2Samuel",
                "1Chronicles",
                "2Chronicles",
                "1Timothy",
                "2Timothy",
                "1Thessalonians",
                "2Thessalonians",
                "Jude",
                "Judges",
            ]:
                self.assertEqual(validations.verify_book(word, K.BOOKS), each)

    def test_verify_book_chapter(self):
        for book, n_chapters in K.TEST_BOOK_CHAPTERS.items():
            self.assertTrue(
                validations.verify_book_chapter(book, str(n_chapters))
            )

    def test_verify_language(self):
        self.assertEqual(validations.verify_language("sparnish"), "Spanish")

    def test_verify_version(self):
        self.assertEqual(
            validations.verify_version("KJV").replace(" ", ""),
            "KingJamesVersion",
        )

    def test_translate_message(self):
        self.assertEqual(
            validations.translate_message("hola", "English", "Spanish"),
            "hello",
        )
