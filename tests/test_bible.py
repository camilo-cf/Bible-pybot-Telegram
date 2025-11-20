"""
    Unit tests for the Bible class.
"""
import unittest
import random
import sys
import string

sys.path.append("./src/")
from utils import bible


class TestBible(unittest.TestCase):
    def test_get_chapter(self):
        self.assertNotEqual(bible.get_chapter("Genesis", 1), None)

    def test_get_message(self):
        # v2 API doesn't include \r\n line endings
        GEN_1_1 = [
            "1 In the beginning God created the heaven and the earth."
        ]
        self.assertEqual(
            bible.get_message("Genesis 1:1."),
            GEN_1_1,
        )
        self.assertEqual(
            bible.get_message("Genesis 1:1"),
            GEN_1_1,
        )
        # Check that Genesis 1:1 is in the full Genesis 1 chapter
        result = bible.get_message("Genesis 1")[0]
        self.assertIn("In the beginning God created", result)
        self.assertEqual(
            bible.get_message("Genesis 100:100"),
            ["Error - Passage not found"],
        )
        self.assertEqual(
            bible.get_message("Genesis"),
            ["Error - Verify the chapter of the passage"],
        )

    def test_next_chapter(self):
        self.assertEqual(bible.get_next_chapter("John 1"), "John 2")
        self.assertEqual(bible.get_next_chapter("John 1."), "John 2")
        self.assertEqual(bible.get_next_chapter("John 21"), "Acts 1")
        self.assertEqual(bible.get_next_chapter("John 21."), "Acts 1")
        self.assertEqual(bible.get_next_chapter("John"), "Genesis 1")
