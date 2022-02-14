"""
    Database functions for the user management
"""
import sqlite3


def create_db():
    '''
    Create or initialize the database for the application

    Returns:
        connection, cursor
            Objects to interact and manipulate a dabatase.
    '''

    connection = sqlite3.connect("data/users.db")
    cursor = connection.cursor()
    sql_command = """
    CREATE TABLE IF NOT EXISTS users ( 
        id          INTEGER         PRIMARY KEY     NOT NULL, 
        name        TEXT            NOT NULL, 
        status      BOOLEAN         DEFAULT 0,
        book        VARCHAR(30)     DEFAULT Genesis, 
        chapter     TINYINT         DEFAULT 1, 
        language    TEXT            DEFAULT English,
        b_version   TEXT            DEFAULT akjv,
        mod_book    BOOLEAN         DEFAULT 0,
        mod_chapter BOOLEAN         DEFAULT 0, 
    mod_language    BOOLEAN         DEFAULT 0,
    mod_b_version   BOOLEAN         DEFAULT 0,
        verse       BOOLEAN         DEFAULT 0
        );
    """
    cursor.execute(sql_command)
    connection.commit()
    return connection, cursor


def add_user(connection, cursor, user_id, name):
    '''
    Add a new user in the database

    Args:
        connection: Database connection
        cursor: Database cursor
        user_id (int): ID in telegram for the user chat
        name (str): Name of the user
    '''

    try:
        cursor.execute("INSERT INTO users(id, name) VALUES(?,?);", (user_id, name))
        connection.commit()
    except sqlite3.Error:
        print("Error in the query - the user already exists")


def get_subscribed_user(cursor):
    '''
    Get the id list of the subscribed users

    Args:
        cursor: Database cursor

    Return:
        List of subscribed users IDs
    '''

    cursor.execute("SELECT id FROM users WHERE status = ?;", (1,))
    return cursor.fetchall()


def set_language(connection, cursor, lang, user_id):
    '''
    Set a language for a given user

    Args:
        connection: Database connection
        cursor: Database cursor
        language (str): Name of the desired user language
        user_id (int): ID of the user
    '''

    try:
        cursor.execute(
            "UPDATE users SET language = ? where id = ?;", (lang, user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def get_language(cursor, user_id):
    '''
    Get the language of a given user

    Args:
        cursor: Database cursor
        user_id (int): ID of the user

    Return:
        Language of the user
    '''
    try:
        cursor.execute("SELECT language FROM users WHERE id = ?;", (user_id,))
        return cursor.fetchall()[0][0]
    except sqlite3.Error:
        return "English"

# modificate the language modificator value (mod_language) in the db
def set_mod_language(connection, cursor, user_id):
    """
        TODO: Add description
    """
    try:
        result = int(not bool(get_mod_language(cursor, user_id)))
        cursor.execute(
            "UPDATE users SET mod_language = ? where id = ?;", (result, user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def get_mod_language(cursor, user_id):  # get the mod_language for the id
    """
        TODO: Add description
    """
    cursor.execute("SELECT mod_language FROM users WHERE id = ?;", (user_id,))
    return cursor.fetchall()[0][0]


def set_status(connection, cursor, status, user_id):  # save the subscription status in the db
    """
        TODO: Add description
    """
    try:
        cursor.execute(
            "UPDATE users SET status = ? where id = ?;", (status, user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def get_status(cursor, user_id):  # get the registry/subscription status for the id
    """
        TODO: Add description
    """
    try:
        cursor.execute("SELECT status FROM users WHERE id = ?;", (user_id,))
        return cursor.fetchall()[0][0]
    except sqlite3.Error:
        return 0


def set_book(connection, cursor, book, user_id):  # save the book in the db
    """
        TODO: Add description
    """
    try:
        cursor.execute("UPDATE users SET book = ? where id = ?;", (book, user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def get_book(cursor, user_id):  # get the book for the id
    """
        TODO: Add description
    """
    cursor.execute("SELECT book FROM users WHERE id = ?;", (user_id,))
    return cursor.fetchall()[0][0]


# modificate the book modificator value (mod_book) in the db
def set_mod_book(connection, cursor, user_id):
    """
        TODO: Add description
    """
    try:
        cursor.execute("UPDATE users SET mod_book = ? where id = ?;",
                       (not(bool(get_mod_book(cursor, user_id))), user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def get_mod_book(cursor, user_id):  # get the mod_book for the id
    """
        TODO: Add description
    """
    cursor.execute("SELECT mod_book FROM users WHERE id = ?;", (user_id,))
    return cursor.fetchall()[0][0]


def set_chapter(connection, cursor, chapter, user_id):  # save the chapter number in the db
    """
        TODO: Add description
    """
    try:
        cursor.execute(
            "UPDATE users SET chapter = ? where id = ?;", (chapter, user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def get_chapter(cursor, user_id):  # get the chapter for the id
    """
        TODO: Add description
    """
    cursor.execute("SELECT chapter FROM users WHERE id = ?;", (user_id,))
    return cursor.fetchall()[0][0]


# modificate the chapter modificator value (mod_chapter) in the db
def set_mod_chapter(connection, cursor, user_id):
    """
        TODO: Add description
    """
    try:
        cursor.execute("UPDATE users SET mod_chapter = ? where id = ?;",
                       (not(bool(get_mod_chapter(cursor, user_id))), user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def get_mod_chapter(cursor, user_id):  # get the chapter for the id
    """
        TODO: Add description
    """
    cursor.execute("SELECT mod_chapter FROM users WHERE id = ?;", (user_id,))
    return cursor.fetchall()[0][0]


def set_bible_version(connection, cursor, version, user_id):  # save the version to read
    """
        TODO: Add description
    """
    try:
        cursor.execute(
            "UPDATE users SET b_version = ? where id = ?;", (version, user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def get_bible_version(cursor, user_id):  # get the bible version for the id
    """
        TODO: Add description
    """
    cursor.execute("SELECT b_version FROM users WHERE id = ?;", (user_id,))
    return cursor.fetchall()[0][0]


# modificate the bible_version modificator value (mod_b_version) in the db
def set_mod_bible_version(connection, cursor, user_id):
    """
        TODO: Add description
    """
    try:
        cursor.execute("UPDATE users SET mod_b_version = ? where id = ?;",
                       (not(bool(get_mod_bible_version(cursor, user_id))), user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def get_mod_bible_version(cursor, user_id):  # get the mod bible_version for the id
    """
        TODO: Add description
    """
    cursor.execute("SELECT mod_b_version FROM users WHERE id = ?;", (user_id,))
    return cursor.fetchall()[0][0]


# modificate the verse modificator value (verse) in the db
def set_verse(connection, cursor, user_id):
    """
        TODO: Add description
    """
    try:
        cursor.execute("UPDATE users SET verse = ? where id = ?;",
                       (not(bool(get_verse(cursor, user_id))), user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def get_verse(cursor, user_id):  # get the mod verse for the id
    """
        TODO: Add description
    """
    cursor.execute("SELECT verse FROM users WHERE id = ?;", (user_id,))
    return cursor.fetchall()[0][0]


def set_mod_default(connection, cursor, user_id):
    """
        TODO: Add description
    """
    try:
        cursor.execute(
            """UPDATE users
                    SET mod_book  = ?,  mod_chapter = ?, mod_language = ?, mod_b_version = ?
                    WHERE id = ?;""",
            (0, 0, 0, 0, user_id))
        connection.commit()
    except sqlite3.Error:
        print("Error - verify the entry")


def verify_id(cursor, user_id):
    '''
    Verify if an user exists
    '''
    cursor.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
    response = cursor.fetchall()
    if len(response) == 0:
        exist = False
    else:
        exist = True
    return exist


def read_db(cursor):
    '''
    Read all the database
    '''
    cursor.execute("SELECT * FROM users;")
    response = cursor.fetchall()
    return response


def close_db(connection):
    '''
    Close the database connection

    Args:
        connection
    '''
    connection.close()
