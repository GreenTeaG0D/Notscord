##~~ DEFINITION SECTION BELOW ~~##
"""
The database tester runs a series of actions thru database access and shows any failures (safe or unsafe)
"""


##~~ IMPORT SECTION BELOW ~~##

import database_access as dba
import db

##~~ WIPE DATABASE SECTION BELOW ~~##

db.clear_tables()


##~~ TESTER SECTION BELOW ~~##

def tester(funcs:list) -> tuple:    
    safe_failures = {}
    unsafe_failures = {}
    for i in range(len(funcs)):
        func = funcs[i][0]
        args = funcs[i][1:]
        try:
            successful = func(*args)
            if not successful:
                safe_failures[func] = args
        except Exception as e:
            unsafe_failures[func] = e
    return (safe_failures, unsafe_failures)


##~~ TESTER DATA SECTION BELOW ~~##

get_private_result = tester([
                    [dba.create_user, 1, "username 1", "hashed password 1", "email1@gmail.com"],
                    [dba.create_user, 2, "username 2", "hashed_password_2", "email2@gmail.com"],
                    [dba.send_private_message, 1, 1, 2, "message 1 from 1 to 2"],
                    [dba.send_private_message, 2, 2, 1, "message 2 from 2 to 1"],
                    [dba.send_private_message, 3, 1, 2, "message 3 from 1 to 2"],
                    [dba.send_private_message, 4, 2, 1, "message 4 from 2 to 1"],
                    [dba.send_private_message, 5, 1, 2, "message 5 from 1 to 2"],
                    [dba.send_private_message, 6, 2, 1, "message 6 from 2 to 1"],
                    [dba.send_private_message, 7, 1, 2, "message 7 from 1 to 2"],
                    [dba.send_private_message, 8, 2, 1, "message 8 from 2 to 1"],
                    [dba.send_private_message, 9, 1, 2, "message 9 from 1 to 2"],
                    [dba.send_private_message, 10, 2, 1, "message 10 from 2 to 1"],
                    [dba.send_private_message, 11, 1, 2, "message 11 from 1 to 2"],
                    [dba.send_private_message, 12, 2, 1, "message 12 from 2 to 1"],
                    [dba.delete_private_message, 1],
                    [dba.delete_private_message, 3],
                    [dba.delete_private_message, 5],
                    [dba.delete_private_message, 7],
                    [dba.delete_private_message, 9],
                    [dba.delete_private_message, 11],
                   ])

response = dba.get_private_message(1, 2, 10)
print([item[3] for item in response])
db.clear_tables()

full_result = tester([
                    [dba.create_user, 1, "username 1", "hashed password 1", "email1@gmail.com"],
                    [dba.create_user, 2, "username 2", "hashed_password_2", "email2@gmail.com"],
                    [dba.send_private_message, 1, 1, 2, "message from 1 to 2"],
                    [dba.send_private_message, 2, 2, 1, "message from 2 to 1"],
                    [dba.modify_private_message, 1, "modified message 1"],
                    [dba.modify_private_message, 2, "modified message 2"],
                    [dba.delete_private_message, 1],
                    [dba.delete_private_message, 2],
                    [dba.add_friend, 1, 2],
                    
                    [dba.create_server, 1, "server 1"],
                    [dba.join_server, 1, 1],
                    [dba.join_server, 1, 2],
                    [dba.send_server_message, 1, 1, 1, "message 1, server 1, user 1"],
                    [dba.send_server_message, 2, 1, 1, "message 2, server 1, user 1"],
                    [dba.send_server_message, 3, 1, 2, "message 3, server 1, user 2"],
                    [dba.send_server_message, 4, 1, 2, "message 4, server 1, user 2"],
                    [dba.modify_server_message, 1, 1, "modified message 1, server 1"],
                    [dba.modify_server_message, 2, 1, "modified message 2, server 1"],
                    [dba.modify_server_message, 3, 1, "modified message 3, server 1"],
                    [dba.modify_server_message, 4, 1, "modified message 4, server 1"],
                    [dba.delete_server_message, 1, 1],
                    [dba.delete_server_message, 2, 1],
                    [dba.delete_server_message, 3, 1],
                    [dba.delete_server_message, 4, 1],
                    
                    [dba.create_server, 2, "server 2"],
                    [dba.join_server, 2, 1],
                    [dba.join_server, 2, 2],
                    [dba.send_server_message, 1, 2, 1, "message 1, server 2, user 1"],
                    [dba.send_server_message, 2, 2, 1, "message 2, server 2, user 1"],
                    [dba.send_server_message, 3, 2, 2, "message 3, server 2, user 2"],
                    [dba.send_server_message, 4, 2, 2, "message 4, server 2, user 2"],
                    [dba.modify_server_message, 1, 2, "modified message 1, server 2"],
                    [dba.modify_server_message, 2, 2, "modified message 2, server 2"],
                    [dba.modify_server_message, 3, 2, "modified message 3, server 2"],
                    [dba.modify_server_message, 4, 2, "modified message 4, server 2"],
                    [dba.delete_server_message, 1, 2],
                    [dba.delete_server_message, 2, 2],
                    [dba.delete_server_message, 3, 2],
                    [dba.delete_server_message, 4, 2],
])


##~~ RESPONSE SECTION BELOW ~~##

print(f"safe failures: {full_result[0]}")
print(f"unsafe failures: {full_result[1]}")