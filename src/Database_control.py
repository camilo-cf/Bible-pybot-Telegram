import sqlite3

def create_db():
    '''
    Create or initialize the database for the application

    Returns:
        connection, cursor 
            Objects to interact and manipulate a dabatase 
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


def add_user(connection, cursor, id, name):
    '''
    Add a new user in the database

    Args:
        connection: Database connection
        cursor: Database cursor
        id (int): ID in telegram for the user chat
        name (str): Name of the user
    '''

    try:
        cursor.execute("INSERT INTO users(id, name) VALUES(?,?);", (id, name))
        connection.commit()
    except:
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


def set_language(connection, cursor, lang, id):
    '''
    Set a language for a given user

    Args:
        connection: Database connection
        cursor: Database cursor
        language (str): Name of the desired user language
        id    
    '''

    try:
        cursor.execute("UPDATE users SET language = ? where id = ?;", (lang, id))
        connection.commit()
    except:
        print("Error - verify the entry")


def get_language(cursor, id):
    '''
    Get the language of a given user

    Args:
        cursor: Database cursor
        id 
    
    Return:
        Language of the user
    '''
    try:
        cursor.execute("SELECT language FROM users WHERE id = ?;", (id,))
        return cursor.fetchall()[0][0]
    except:
        return "English"


def set_mod_language(connection, cursor, id):#modificate the language modificator value (mod_language) in the db
    try:
        result = (int(not(bool(get_mod_language(cursor, id)))))
        cursor.execute("UPDATE users SET mod_language = ? where id = ?;", (result, id))
        connection.commit()
    except:
        print("Error - verify the entry")


def get_mod_language(cursor, id):# get the mod_language for the id
    cursor.execute("SELECT mod_language FROM users WHERE id = ?;", (id,))
    return cursor.fetchall()[0][0]


def set_status(connection, cursor, status, id):#save the subscription status in the db
    try:
        cursor.execute("UPDATE users SET status = ? where id = ?;", (status, id))
        connection.commit()
    except:
        print("Error - verify the entry")


def get_status(cursor, id):# get the registry/subscription status for the id
    try:
        cursor.execute("SELECT status FROM users WHERE id = ?;", (id,))
        return cursor.fetchall()[0][0]
    except:
        return 0



def set_book(connection, cursor, book, id):#save the book in the db 
    try:
        cursor.execute("UPDATE users SET book = ? where id = ?;", (book, id))
        connection.commit()
    except:
        print("Error - verify the entry")


def get_book(cursor, id):# get the book for the id
    cursor.execute("SELECT book FROM users WHERE id = ?;", (id,))
    return cursor.fetchall()[0][0]


def set_mod_book(connection, cursor, id):#modificate the book modificator value (mod_book) in the db
    try:

        cursor.execute("UPDATE users SET mod_book = ? where id = ?;", (not(bool(get_mod_book(cursor, id))), id))
        connection.commit()
    except:
        print("Error - verify the entry")


def get_mod_book(cursor, id):# get the mod_book for the id
    cursor.execute("SELECT mod_book FROM users WHERE id = ?;", (id,))
    return cursor.fetchall()[0][0]


def set_chapter(connection, cursor, chapter, id):#save the chapter number in the db 
    try:
        cursor.execute("UPDATE users SET chapter = ? where id = ?;", (chapter, id))
        connection.commit()
    except:
        print("Error - verify the entry")

    
def get_chapter(cursor, id):# get the chapter for the id
    cursor.execute("SELECT chapter FROM users WHERE id = ?;", (id,))
    return cursor.fetchall()[0][0]


def set_mod_chapter(connection, cursor, id):#modificate the chapter modificator value (mod_chapter) in the db
    try:
        cursor.execute("UPDATE users SET mod_chapter = ? where id = ?;", (not(bool(get_mod_chapter(cursor, id))), id))
        connection.commit()
    except:
        print("Error - verify the entry")


def get_mod_chapter(cursor, id):# get the chapter for the id
    cursor.execute("SELECT mod_chapter FROM users WHERE id = ?;", (id,))
    return cursor.fetchall()[0][0]


def set_bible_version(connection, cursor, version, id):#save the version to read
    try:
        cursor.execute("UPDATE users SET b_version = ? where id = ?;", (version, id))
        connection.commit()
    except:
        print("Error - verify the entry")

    
def get_bible_version(cursor, id):# get the bible version for the id
    cursor.execute("SELECT b_version FROM users WHERE id = ?;", (id,))
    return cursor.fetchall()[0][0]


def set_mod_bible_version(connection, cursor, id):#modificate the bible_version modificator value (mod_b_version) in the db
    try:
        cursor.execute("UPDATE users SET mod_b_version = ? where id = ?;", (not(bool(get_mod_bible_version(cursor, id))), id))
        connection.commit()
    except:
        print("Error - verify the entry")


def get_mod_bible_version(cursor, id):# get the mod bible_version for the id
    cursor.execute("SELECT mod_b_version FROM users WHERE id = ?;", (id,))
    return cursor.fetchall()[0][0]


def set_verse(connection, cursor, id):#modificate the verse modificator value (verse) in the db
    try:
        cursor.execute("UPDATE users SET verse = ? where id = ?;", (not(bool(get_verse(cursor, id))), id))
        connection.commit()
    except:
        print("Error - verify the entry")


def get_verse(cursor, id):# get the mod verse for the id
    cursor.execute("SELECT verse FROM users WHERE id = ?;", (id,))
    return cursor.fetchall()[0][0]


def set_mod_default(connection, cursor, id):
    try:
        cursor.execute("UPDATE users SET mod_book  = ?,  mod_chapter = ?, mod_language = ?, mod_b_version = ? WHERE id = ?;", (0, 0, 0, 0, id))
        connection.commit()
    except:
        print("Error - verify the entry")


def verify_id(cursor, id):
    '''
    Verify if an user exists
    '''
    cursor.execute("SELECT * FROM users WHERE id = ?;", (id,))
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


