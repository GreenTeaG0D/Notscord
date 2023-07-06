##~~ DEFINITION SECTION BELOW ~~##

"""
The database access module is used to normalise access to the database
"""


##~~ IMPORT SECTION BELOW ~~##

import sqlite3
import time
import re


##~~ STUPIDLY UNSAFE TESTING BELOW ~~##
def clear_tables():
    import db
    db.clear_tables()
    print(f"tables cleared")
    return True


##~~ VALIDATION SECTION BELOW ~~##

def value_in_table(table:str, field:str, value:str) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    return cursor.execute(f"SELECT {field} FROM {table} WHERE {field} == '{value}'").fetchone() != None
    
def composite_key_exists(table:str, first_field:str, second_field:str, first_key:int, second_key:int) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    return cursor.execute(f"""SELECT {first_field}, {second_field}
                                FROM {table}
                                WHERE {first_field} == '{first_key}'
                                AND {second_field} == '{second_key}'
                        """).fetchone() != None
    
def valid_email(email:str) -> bool:
    regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    return re.fullmatch(regex, email)


##~~ USER SECTION BELOW ~~##

def create_user(uuid:int, username:str, hashed_password:str, email:str) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    
    if value_in_table("user", "uuid", uuid):
        print("uuid taken")
        return False
    
    elif not valid_email(email):
        print("email invalid")
        return False

    else:
        created_at = time.time()
        modified_at = None
        cursor.execute(f"INSERT INTO user VALUES ('{uuid}', '{username}', '{hashed_password}', '{email}', '{created_at}', '{modified_at}')")
        connection.commit()
        print(f"CREATED: {uuid}")
        return True
   
def send_private_message(umid:int, from_uuid:int, to_uuid:int, content:str) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    
    if value_in_table("pmsg", "umid", umid):
        print("umid taken")
        return False
    
    else:
        created_at = time.time()
        modified_at = None
        deleted = 0
        cursor.execute(f"INSERT INTO pmsg VALUES ('{umid}', '{from_uuid}', '{to_uuid}', '{content}', '{created_at}', '{modified_at}', '{deleted}')")
        connection.commit()
        print(f"SENT: {umid}")
        return True

def modify_private_message(umid:int, content:str) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    
    if not value_in_table("pmsg", "umid", umid):
        print("message does not exist")
        return False
    
    else:
        modified_at = time.time()
        cursor.execute(f"UPDATE pmsg SET content = '{content}', modified_at = '{modified_at}' WHERE umid = '{umid}'")
        connection.commit()
        print(f"MODIFIED: {umid}")
        return True

def delete_private_message(umid:int) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    
    if not value_in_table("pmsg", "umid", umid):
        print("message does not exist")
        return False
    
    else:
        cursor.execute(f"""UPDATE pmsg
                       SET deleted = 1
                       WHERE umid = '{umid}'""")
        print(f"DELETED: {umid}")
        connection.commit()
        return True

def get_private_message(from_uuid:int, to_uuid: int, count:int) -> list:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    print(f"GETTING: between {from_uuid} and {to_uuid}")
    return cursor.execute(f"""
                          SELECT *
                          FROM pmsg
                          WHERE sender_uuid == '{from_uuid}'
                          AND target_uuid == '{to_uuid}'
                          AND deleted == 0
                          OR sender_uuid == '{to_uuid}'
                          AND target_uuid = '{from_uuid}'
                          AND deleted == 0
                          LIMIT {count}
                          """).fetchall()

def add_friend(from_uuid:int, to_uuid:int) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    
    if composite_key_exists("friend", "first_uuid", "second_uuid", from_uuid, to_uuid):
        print("already friends")
        return False
    
    else:
        created_at = time.time()
        cursor.execute(f"INSERT INTO friend VALUES ('{from_uuid}', '{to_uuid}', '{created_at}')")
        connection.commit()
        print(f"FRIENDED: between {from_uuid} and {to_uuid}")
        return True


##~~ SERVER SECTION BELOW ~~##

def create_server(usid:int, server_name:str) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    
    if value_in_table("server", "usid", usid):
        print("usid taken")
        return False
    
    else:
        created_at = time.time()
        cursor.execute(f"INSERT INTO server VALUES ('{usid}', '{server_name}', '{created_at}')")
        connection.commit()
        print(f"SERVER CREATED: {usid}")
        return True

def send_server_message(umid:int, usid:int, uuid:int, content:str) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    
    if composite_key_exists("smsg", "umid", "usid", umid, usid):
        print("umid taken")
        return False
    
    else:
        created_at = time.time()
        modified_at = None
        deleted = 0
        cursor.execute(f"INSERT INTO smsg VALUES ('{umid}', '{usid}', '{uuid}', '{content}', '{created_at}', '{modified_at}', '{deleted}')")
        connection.commit()
        print(f"SENT: {umid} in server {usid}")
        return True

def modify_server_message(umid:int, usid:int, content:str) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    
    if not composite_key_exists("smsg", "umid", "usid", umid, usid):
        print("message does not exist in server")
        return False
    
    else:
        modified_at = time.time()
        cursor.execute(f"UPDATE smsg SET content = '{content}', modified_at = '{modified_at}' WHERE umid = '{umid}' AND usid = '{usid}'")
        connection.commit()
        print(f"MODIFIED: {umid} in {usid}")
        return True

def delete_server_message(umid:int, usid:int) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    
    if not composite_key_exists("smsg", "umid", "usid", umid, usid):
        print("message does not exist in server")
        return False
    
    else:
        cursor.execute(f"UPDATE smsg SET deleted = 1 WHERE umid = '{umid}' AND usid = '{usid}'")
        connection.commit()
        print(f"DELETED: {umid} in {usid}")
        return True 

def get_server_message(usid:int, count:int) -> list:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    print(f"GETTING: in {usid}")
    return cursor.execute(f"""
                          SELECT *
                          FROM smsg
                          WHERE usid == {usid}
                          LIMIT {count}
                          """).fetchall()

def join_server(usid:int, uuid:int) -> bool:
    connection = sqlite3.connect('DB.db')
    cursor = connection.cursor()
    
    if composite_key_exists("smbr", "uuid", "usid", uuid, usid):
        print("user already in server")
        return False
    
    else:
        created_at = time.time()
        cursor.execute(f"INSERT INTO smbr VALUES ('{uuid}', '{usid}', '{created_at}')")
        connection.commit()
        print(f"JOINED: {uuid} joined {usid}")
        return True