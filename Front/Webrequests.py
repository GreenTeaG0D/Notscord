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
    
    def get_response(self) -> str:
        return self.response

    def get_status(self) -> int:
        return self.status_code

    def get_content(self) -> str:
        return self.content

    def get_text(self) -> str:
        return self.text

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


class user():
    def __init__(self, username:str, hashed_password:str, email:str):
        self.username = username
        self.hashed_password = hashed_password
        self.email = email
        self.uuid = self.create_user()
        self.my_servers = {}

    def create_user(self) -> str:
        data = {
                'username':self.username,
                'hashed_password':self.hashed_password,
                'email':self.email
                }
        return post('/create/user', data).parse('uuid')

    def get_uuid_by_username(recipient:int|str) -> int:
        if type(recipient) == str:
            recipient = get(f'/search/user/{recipient}').parse('uuid')
        return recipient 

    def send_private_message(self, recipient:int|str, content:str) -> int:
        recipient = self.get_uuid_by_username(recipient)
        data = {'sender_uuid':self.uuid, 'content':content}
        umid = post(f'/private/{recipient}', data).parse('umid')
        return umid

    def modify_private_message(self, recipient:int|str, umid:int, content:str) -> bool:
        recipient = self.get_uuid_by_username(recipient)
        data = {'sender_uuid':self.uuid, 'umid':umid, 'content':content}
        response = put(f'/private/{recipient}', data)
        return response.is_valid_response()

    def delete_private_message(self, recipient:int|str, umid:int) -> bool:
        recipient = self.get_uuid_by_username(recipient)
        data = {'sender_uuid':self.uuid, 'umid':umid}
        response = delete(f'/private/{recipient}', data)
        return response.status_code < 400
    
    def get_private_messages(self, recipient:int|str, count:int) -> dict:
        recipient = self.get_uuid_by_username(recipient)
        data = {'sender_uuid':self.uuid, 'count':count}
        messages = get(f'/private/{recipient}', data).parse('messages')
        return messages

    def add_friend(self, recipient:int|str) -> bool:
        recipient = self.get_uuid_by_username(recipient)
        data = {'sender_uuid':self.uuid}
        response = post(f'/friend/{recipient}', data)
        return response.is_valid_response
    
    
    def get_usid_by_name(recipient:int|str) -> int:
        if type(recipient) == str:
            recipient = get(f'/search/server/{recipient}').parse('uuid')
        return recipient

    def create_server(self, server_name:str) -> int:
        data = {'server_name':server_name}
        usid =  post('/create/server', data).parse('usid')
        self.my_servers[server_name] = usid
        return usid
        
    def send_server_message(self, server:int|str, content:str) -> int:
        usid = self.get_usid_by_name(server)
        data = {'uuid':self.uuid, 'content':content}
        return post(f'/server/{usid}', data = data).parse('umid')
    
    def update_server_message(self, server:int|str, umid:int, content:str) -> bool:
        usid = self.get_usid_by_name(server)
        data = {'umid':umid, 'content':content}
        return put(f'/server/{usid}', data = data).is_valid_response()
    
    def delete_server_message(self, server:int|str, umid:int) -> bool:
        usid = self.get_usid_by_name(server)
        data = {'umid':umid}
        return delete(f'/server/{usid}', data = data).is_valid_response()
    
    def get_server_messages(self, server:int|str, count:int) -> dict:
        usid = self.get_usid_by_name(server)
        data = {'count':count}
        return get(f'/server/{usid}', data = data).parse('messages')