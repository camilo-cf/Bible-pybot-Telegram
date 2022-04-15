"""File with all the SQL queries
"""
CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS users ( 
            id          INTEGER         PRIMARY KEY     NOT NULL, 
            name        TEXT            NOT NULL, 
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

ADD_USER = """INSERT INTO users(id, name) VALUES ('{}','{}');"""
GET_USER = """SELECT * FROM users WHERE id = '{}';"""
GET_USERS = "SELECT id FROM users WHERE status = '{}';"
SET_LANGUAGE = "UPDATE users SET language = '{}' where id = '{}';"
GET_LANGUAGE = "SELECT language FROM users WHERE id = '{}';"
SET_MOD_LANGUAGE = "UPDATE users SET mod_language = '{}' where id = '{}';"
GET_MOD_LANGUAGE = "SELECT mod_language FROM users WHERE id = '{}';"
SET_BOOK = "UPDATE users SET book = '{}' where id = '{}';"
GET_BOOK = "SELECT book FROM users WHERE id = '{}';"
SET_MOD_BOOK = "UPDATE users SET mod_book = '{}' where id = '{}';"
GET_MOD_BOOK = "SELECT mod_book FROM users WHERE id = '{}';"
SET_CHAPTER = "UPDATE users SET chapter = '{}' WHERE id = '{}';"
GET_CHAPTER = "SELECT chapter FROM users WHERE id = '{}';"
SET_MOD_CHAPTER = "UPDATE users SET mod_chapter = '{}' where id = '{}';"
GET_MOD_CHAPTER = "SELECT mod_chapter FROM users WHERE id = '{}';"
SET_BIBLE_VERSION = "UPDATE users SET b_version = '{}' WHERE id = '{}';"
GET_BIBLE_VERSION = "SELECT b_version FROM users WHERE id = '{}';"
SET_MOD_BIBLE_VERSION = (
    "UPDATE users SET mod_b_version = '{}' where id = '{}';"
)
GET_MOD_BIBLE_VERSION = "SELECT mod_b_version FROM users WHERE id = '{}';"
SET_VERSE = "UPDATE users SET verse = '{}' where id = '{}';"
GET_VERSE = "SELECT verse FROM users WHERE id = '{}';"
SET_MOD_DEFAULT = """UPDATE users
                    SET mod_book  = 0,  mod_chapter = 0, mod_language = 0, mod_b_version = 0
                    WHERE id = '{}';"""
VERIFY_ID = "SELECT * FROM users WHERE id = '{}';"
READ_DB = "SELECT * FROM users;"
GET_SUBSCRIBED_USERS = "SELECT id FROM users WHERE status = 1;"
