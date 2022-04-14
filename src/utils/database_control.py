"""
    Database functions for the user management
"""
import sqlite3
import sys

sys.path.append("./src/")
import utils.queries as Q


class UsersDB:
    """Class to control the users database"""

    def __init__(self, db_path: str = "data/users.db"):
        """Initialize the database for the application

        Args:
            db_path (str, optional): _description_. Defaults to "data/users.db".
        """
        self.connection = sqlite3.connect(db_path)
        cursor = self.connection.cursor()
        cursor.execute(Q.CREATE_TABLE.replace("\n", ""))
        cursor.close()
        self.connection.commit()

    def close(self) -> None:
        """Close the connection on exit"""
        self.connection.close()

    def execute_query(self, query: str) -> bool:
        """Executes a query in the database.

        Args:
            query (str):
                The query to be executed in string.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query.replace("\n", ""))
            cursor.close()
            self.connection.commit()
        except Exception:
            print(f"Error: {Exception}")

    def fetch_query(self, query: str) -> str:
        """Fetches the result of a query in the database.

        Args:
            query (str):
                The query to be fetched in string.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception:
            print(f"Error: {Exception}")
        finally:
            cursor.close()
