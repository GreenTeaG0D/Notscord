##~~ DEFINITION SECTION BELOW ~~##
"""
The db module is used to create and/or clear the database and tables (outlined in the changelog section)
"""


##~~ CHANGELOG SECTION BELOW ~~##

"""
    TABLES MIN REQ (works):

    USER - IDENTIFIER (UUID)
    P. Msg - IDENTIFIER (UMID), FROM (UUID), TO (UUID)
    FRIEND - YOU (UUID), FRIEND (UUID)

    SERVER - IDENTIFIER (USID)
    S. Msg - IDENTIFIER (UMID), IN (USID)
    S. Mbr - YOU (UUID), IN (USID)


    TABLES L_MED (works):

    USER - USERNAME (username)
    P. Msg - CONTENT (message)

    SERVER - NAME (server name)
    S. Msg - CONTENT (message)


    TABLES M_MED (works):
    P. Msg - SENT (created at), UPDATED (modified at)
    S. Msg - SENDER (UUID), SENT (created at), UPDATED (modified at)


    TABLES U_MED (works):
    USER - PW (hashed password), EMAIL (email), SIGNED UP (created at), LOGGED IN (last login)
    P. Msg - DELETED (deleted)
    FRIEND - FRIENDED AT (created at)

    SERVER - CREATED AT (created at)
    S. Msg - DELETED (deleted)
    S. Mbr - JOINED AT (created at)
"""


##~~ IMPORT SECTION BELOW ~~##

import sqlite3


##~~ DATABASE CONNECTION SECTION BELOW ~~##

connection = sqlite3.connect('DB.db')
cursor = connection.cursor()


##~~ TABLE CREATION SECTION BELOW ~~##

def create_tables() -> bool:
    tbl_user = """
        CREATE TABLE IF NOT EXISTS user (
            uuid INTEGER PRIMARY KEY,
            username TEXT,
            hashed_password TEXT,
            email TEXT,
            created_at REAL,
            last_login REAL
        )
    """

    tbl_pmsg = """
        CREATE TABLE IF NOT EXISTS pmsg (
            umid INTEGER PRIMARY KEY,
            sender_uuid INTEGER,
            target_uuid INTEGER,
            content TEXT,
            created_at REAL,
            modified_at REAL,
            deleted INTEGER
        )
    """

    tbl_friend = """
        CREATE TABLE IF NOT EXISTS friend (
            first_uuid INTEGER,
            second_uuid INTEGER,
            created_at REAL
        )
    """

    tbl_server = """
        CREATE TABLE IF NOT EXISTS server (
            usid INTEGER PRIMARY KEY,
            server_name TEXT,
            created_at REAL
        )
    """

    tbl_smsg = """
        CREATE TABLE IF NOT EXISTS smsg (
            umid INTEGER,
            usid INTEGER,
            uuid INTEGER,
            content TEXT,
            created_at REAL,
            modified_at REAL,
            deleted INTEGER
        )
    """

    tbl_smbr = """
        CREATE TABLE IF NOT EXISTS smbr (
            uuid INTEGER,
            usid INTEGER,
            created_at REAL
        )
    """

    tables = [tbl_user, tbl_pmsg, tbl_friend, tbl_server, tbl_smsg, tbl_smbr]
    try:
        for table in tables:
            cursor.execute(table)
        connection.commit()
        return True
    except Exception as e:
        print(e)
        return False


##~~ CLEAR TABLE SECTION BELOW ~~##

def clear_tables() -> bool:
    tables = cursor.execute("SELECT tbl_name FROM sqlite_master").fetchall()
    for table in tables:
        table = table[0].removeprefix("('").removesuffix("'),")
        cursor.execute(f"DROP TABLE {table}")
    connection.commit()
    create_tables()


##~~ RUNNER SECTION BELOW ~~##

create_tables()