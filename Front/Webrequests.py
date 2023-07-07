import requests
import json

url = '127.0.0.1:5000'

class request():
    
    def __init__(self, response:object) -> None:
        self.response = response
        self.status_code = self.response.statuscode
        self.content = self.response.content
        self.text = self.response.text
    
    def parse(self, search:str) -> str:
        return json(self.response).get(search)
    
    def is_valid_response(self) -> bool:
        return self.status_code < 400

class get(request):
    def __init__(self, extension:str, data:dict|None = None) -> None:
        full_url = url + extension
        response = requests.get(url = full_url, data = data, timeout = 3)
        super().__init__(response)

class post(request):
    def __init__(self, extension:str, data:dict|None = None) -> None:
        full_url = url + extension
        response = requests.post(url = full_url, data = data, timeout = 3)
        super().__init__(response)

class put(request):
    def __init__(self, extension:str, data:dict|None = None) -> None:
        full_url = url + extension
        response = requests.put(url = full_url, data = data, timeout = 3)
        super().__init__(response)

class delete(request):
    def __init__(self, extension:str, data:dict|None = None) -> None:
        full_url = url + extension
        response = requests.delete(url = full_url, data = data, timeout = 3)
        super().__init__(response)


class server_action():
    def __init__(self, server_name:str, usid:int|None = None):
        self.server_name = server_name
        if not usid:
            usid = self.create_server()
        self.usid = usid
        self.url = f'/server/{usid}'

    def create_server(self) -> int:
        data = {'server_name':self.server_name}
        usid =  post('/create/server', data).parse('usid')
        return usid

    def get_messages(self, count:int) -> list:
        data = {'count':count}
        return get(self.url, data).parse('messages')
    
class server_message(server_action):
    def __init__(self, server_name: str, usid: int | None = None):
        super().__init__(server_name, usid)
        self.umid = None
        self.uuid = None
    
    def send(self, uuid:int, content:str) -> int:
        self.uuid = uuid
        data = {'uuid':self.uuid, 'content':content}
        self.umid = post(self.url, data).parse('umid')
        return self.umid
    
    def modify(self, content:str):
        data = {'uuid':self.uuid, 'content':content, 'umid':self.umid}
        return put(self.url, data).is_valid_response()
    
    def delete(self):
        data = {'uuid':self.uuid, 'umid':self.umid}
        return delete(self.url, data).is_valid_response()


class user():
    def __init__(self, username:str, hashed_password:str, email:str):
        self.username = username
        self.hashed_password = hashed_password
        self.email = email

    def create_user(self) -> int:
        data = {
                'username':self.username,
                'hashed_password':self.hashed_password,
                'email':self.email
                }
        self.uuid = post('/create/user', data).parse('uuid')
        return self.uuid
    
    def get_messages(self, recipient_uuid:int, count:int):
        data = {'recipient_uuid':recipient_uuid, 'count':count}
        return get(self.url, data).parse('messages')
 
class private_message(user):
    def __init__(self, username: str, hashed_password: str, email: str):
        super().__init__(username, hashed_password, email)
        self.umid = None
        self.recipient_uuid = None
        self.url = f'/private/{self.recipient_uuid}'

    def send(self, recipient_uuid:int, content:str) -> int:
        self.recipient_uuid = recipient_uuid
        data = {'recipient_uuid':recipient_uuid, 'content':content}
        return post(self.url, data).parse('umid')
    
    def modify(self, content:str) -> bool:
        data = {'recipient_uuid':self.recipient_uuid, 'content':content}
        return put(self.url, data).is_valid_response()
    
    def delete(self) -> bool:
        data = {'umid':self.umid, 'recipient_uuid':self.recipient_uuid}
        return delete(self.url, data).is_valid_response()