CREATE_TABLE = """
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

ADD_USER = """INSERT INTO users(id, name) VALUES(?,?);"""