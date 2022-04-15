"""
    Unit tests for the User Database class.
"""
import os
import unittest
import sys

sys.path.append("./src/")
from utils import database_control
import utils.queries as Q


class TestDatabase(unittest.TestCase):
    """Class to test the database."""

    def test_creation_execute_fetch(self):
        """Test db creation, query execution and fetch"""
        TEST_DATA = {
            "id": 1,
            "name": "Name",
        }

        DB_NAME = "./test_db.db"
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)
        db = database_control.UsersDB(DB_NAME)
        db.execute_query(Q.ADD_USER.format(TEST_DATA["id"], TEST_DATA["name"]))
        db_return = db.fetch_query(Q.GET_USER.format(TEST_DATA["id"]))
        self.assertEqual(
            db_return,
            [
                (
                    TEST_DATA["id"],
                    TEST_DATA["name"],
                    "Genesis",
                    1,
                    "English",
                    "akjv",
                    0,
                    0,
                    0,
                    0,
                    0,
                )
            ],
        )
        self.assertTrue(os.path.exists(DB_NAME))
        db.close()
        os.remove(DB_NAME)
