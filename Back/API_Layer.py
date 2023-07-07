##~~ MODULE EXPLAINATION SECTION BELOW ~~##

"""
This is the api layer module, it is used as the interface between the user and the database.
"""


##~~ FLOW OUTLINE BELOW ~~##

"""
Create = /create
Join = /friend | /join
View/Send/Update/Delete = /private/<uuid> | /server/<usid> andand GET, POST, PUT, DELETE
"""


##~~ IMPORTS SECTION BELOW ~~##

from flask import Flask, request
import DB_Access as dba
import random


##~~ APP SETUP BELOW ~~##

app = Flask(__name__)


##~~ STUPID, ONLY FOR TESTING BELOW ~~##

@app.route('/cleartables', methods = ['POST'])
def clear_tables() -> dict and int:
    success = dba.clear_tables()
    response = {'success': success}
    if success:
        return response, 200
    else:
        return response, 400


##~~ ID GENERATION BELOW ~~##

def genID(table:str, field:str) -> int:
    value = random.randint(0, 1000000000000)
    if dba.value_in_table(table, field, value):
        return genID(table, field, value)
    return value

def genCompID(table:str, varField:str, constField:str, constVal:int) -> int:
    num = random.randint(0, 1000000000000)
    if dba.composite_key_exists(table, varField, constField, num, constVal):
        return genCompID(table, varField, constField, constVal)
    return num


##~~ INVALID URL HANDLER BELOW ~~##

@app.errorhandler(Exception)
def page_not_found(Exception) -> dict and int:
    print(f"EXEPTION: {Exception}")
    response = {'message': 'page not found'}
    return response, 404


##~~ ACCOUNT/SERVER CREATION BELOW ~~##

@app.route('/create/<creation>', methods = ['POST'])
def create(creation:str) -> dict and int:
    if creation.lower() == "user":
        username = request.form.get('username')
        hashed_password = request.form.get('hashed_password')
        email = request.form.get('email')
        uuid = genID("user", "uuid")
        success = dba.create_user(uuid, username, hashed_password, email)
        if success:
            response = {"success": success, "uuid": uuid}
            return response, 201
        else:
            response = {"success": success, "uuid": None}
            return response, 400
        
        
    elif creation.lower() == "server":
        server_name = request.form.get('server_name')
        creator_uuid = request.form.get('creator_uuid')
        usid = genID("server", "usid")
        success = dba.create_server(usid, server_name)
        if success:
            dba.join_server(usid, creator_uuid)
            response = {"success": success, "usid": usid}
            return response, 201
        else:
            response = {"success": success, "usid": None}
            return response, 400
    else:
        return {"exception": "must be user or server"}, 404


##~~ USER ACTIONS BELOW ~~##

@app.route('/private/<recipient_uuid>', methods = ['POST', 'PUT', 'DELETE', 'GET'])
def private_message(recipient_uuid:int) -> dict|bool|list and int:
    match request.method:
        case 'POST':
            sender_uuid = request.form.get(key = 'sender_uuid', type = int)
            content = request.form.get(key = 'content', type = str)
            umid = genID("pmsg", "umid")
            success = dba.send_private_message(umid, sender_uuid, recipient_uuid, content)
            if success:
                response = {"success": success, "umid": umid}
                return response, 201
            else:
                response = {"success": success, "umid": None}
                return response, 400

        case 'PUT':
            umid = request.form.get(key = 'umid', type = int)
            content = request.form.get(key = 'content', type = str)
            success = dba.modify_private_message(umid, content)
            response = {"success": success}
            if success:
                return response, 200
            else:
                return response, 400
        
        case 'DELETE':
            umid = request.form.get(key = 'umid', type = int)
            success = dba.delete_private_message(umid)
            response = {"success": success}
            if success:
                return response, 200
            else:
                return response, 400
        
        case 'GET':
            sender_uuid = request.form.get(key = 'sender_uuid', type = int)
            count = request.form.get(key = 'count', type = int)
            messages = dba.get_private_message(sender_uuid, recipient_uuid, count)
            response = {"messages" : messages}
            if messages != None:
                return response, 200
            else:
                return response, 400
            
@app.route('/friend/<recipient_uuid>', methods = ['POST'])
def add_friend(recipient_uuid:int) -> bool and int:
    sender_uuid = request.form.get(key = 'sender_uuid', type = int)
    success = dba.add_friend(recipient_uuid, sender_uuid)
    response = {"success": success}
    if success:
        return response, 200
    else:
        return response, 400

@app.route('/search/user/<username>', methods = ['GET'])
def search_user(username:str) -> int|str and bool:
    uuid = dba.search_user(username)
    if uuid != None:
        response = {'uuid':uuid}
        return response, 200
    else:
        response = {'error':'username not associated with uuid'}
        return response, 400

##~~ SERVER ACTIONS BELOW ~~~#

@app.route('/server/<usid>', methods = ['POST', 'PUT', 'DELETE', 'GET'])
def server_message(usid:int) -> dict|bool|list and int:
    match request.method:
        case 'POST':
            umid = genCompID("smsg", "umid", "usid", usid)
            uuid = request.form.get(key = 'uuid', type = int)
            content = request.form.get(key = 'content', type = str)
            success = dba.send_server_message(umid, usid, uuid, content)
            if success:
                response = {"success": success, "umid": umid}
                return response, 201
            else:
                response = {"success": success, "umid": None}
                return response, 400

        case 'PUT':
            umid = request.form.get(key = 'umid', type = int)
            content = request.form.get(key = 'content', type = str)
            success = dba.modify_server_message(umid, usid, content)
            response = {"success": success}
            if success:
                return response, 200
            else:
                return response, 400
    
        case 'DELETE':
            umid = request.form.get(key = 'umid', type = int)
            success = dba.delete_server_message(umid, usid)
            response = {"success": success}
            if success:
                return response, 200
            else:
                return response, 400

        case 'GET':
            count = request.form.get(key = "count", type = int)
            data = dba.get_server_message(usid, count)
            response = {"messages": data}
            if data != None:
                return response, 200
            else:
                return response, 400

@app.route('/join/<usid>', methods = ['POST'])
def join_server(usid:int) -> bool and int:
    uuid = request.form.get(key = 'uuid', type = int)
    success = dba.join_server(usid, uuid)
    response = {"success": success}
    if success:
        return response, 200
    else:
        return response, 400

@app.route('search/server/<server_name>', methods = ['GET'])
def search_server(server_name:str) -> int|str and bool:
    usid = dba.search_server(server_name)
    if usid != None:
        response = {'uuid':usid}
        return response, 200
    else:
        response = {'error':'server name not associated with usid'}
        return response, 400

##~~ RUNNER BELOW ~~##

app.run()