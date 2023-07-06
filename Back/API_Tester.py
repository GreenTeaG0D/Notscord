import requests
url = "http://127.0.0.1:5000"

def clear_tables_stupid():
    response = requests.post(url = f"{url}/cleartables")
    print(f"RESPONSE clear_tables_stupid: {response}")
    return response

def create_user(username:str, hashed_password:str, email:str) -> int:
    account_data = {
        "username":username,
        "hashed_password": hashed_password,
        "email":email
    }
    response = requests.post(url = f"{url}/create/user", data = account_data)
    print(f"testing response to create_user, {response.json().get('uuid')}")
    return response.json().get('uuid')

def add_friend(sender_uuid:int, recipient_uuid:int) -> bool:
    request_data = {
        "sender_uuid": sender_uuid
    }
    response = requests.post(url = f"{url}/friend/{recipient_uuid}", data = request_data)
    return response

def send_private_message(sender_uuid:int, recipient_uuid:int, content:str) -> int:
    message_data = {
        "sender_uuid": sender_uuid,
        "content": content
    }
    response = requests.post(url = f"{url}/private/{recipient_uuid}", data = message_data)
    return response.json().get('umid')

def modify_private_message(recipient_uuid:int, umid:int, content:str) -> bool:
    message_data = {
        "content": content,
        "umid": umid
    }
    response = requests.put(url = f"{url}/private/{recipient_uuid}", data = message_data)
    return response

def delete_private_message(recipient_uuid:int, umid:int) -> bool:
    request_data = {
        "umid": umid
    }
    response = requests.delete(url = f"{url}/private/{recipient_uuid}", data = request_data)
    return response

def view_private_messages(sender_uuid:int, recipient_uuid:int, count:int) -> list:
    request_data = {
        "sender_uuid": sender_uuid,
        "count": count
    }
    response = requests.get(f"{url}/private/{recipient_uuid}", data = request_data)
    return response.json().get('messages')


def create_server(server_name:str) -> int:
    server_data = {
        "server_name": server_name
    }
    response = requests.post(url = f"{url}/create/server", data = server_data)
    return response.json().get('usid')

def join_server(usid:int, uuid:int) -> bool:
    request_data = {
        "uuid": uuid
    }
    response = requests.post(url = f"{url}/join/{usid}", data = request_data)
    return response

def send_server_message(usid:int, uuid:int, content:str) -> int:
    message_data = {
        "uuid": uuid,
        "content": content
    }
    response = requests.post(url = f"{url}/server/{usid}", data = message_data)
    return response.json().get('umid')

def modify_server_message(usid:int, umid:int, content:str) -> bool:
    message_data = {
        "umid": umid,
        "content": content
    }
    response = requests.put(url = f"{url}/server/{usid}", data = message_data)
    return response

def delete_server_message(usid:int, umid:int) -> bool:
    request_data = {
        "umid": umid
    }
    response = requests.delete(url = f"{url}/server/{usid}", data = request_data)
    return response

def view_server_messages(usid:int, count:int) -> list:
    request_data = {
        "count": count
    }
    response = requests.get(url = f"{url}/server/{usid}", data = request_data)
    return response.json().get('messages')


def user_tester() -> None:
    clear_tables_stupid()

    bertie_uuid = create_user("bertie", "hashed", "email@gmail.com")
    lottie_uuid = create_user("lottie", "hashed", "email@gmail.com")

    add_friend(bertie_uuid, lottie_uuid)
    add_friend(lottie_uuid, bertie_uuid)
    
    b_msg = send_private_message(bertie_uuid, lottie_uuid, "test")
    l_msg = send_private_message(lottie_uuid, bertie_uuid, "test")

    modify_private_message(lottie_uuid, b_msg, "new test")

    comb_msgs = view_private_messages(bertie_uuid, lottie_uuid, 100)
    print(comb_msgs)

    delete_private_message(bertie_uuid, l_msg)

    comb_msgs = view_private_messages(bertie_uuid, lottie_uuid, 100)
    print(comb_msgs)

    delete_private_message(lottie_uuid, b_msg)

    comb_msgs = view_private_messages(bertie_uuid, lottie_uuid, 100)
    print(comb_msgs)

def server_tester() -> None:
    clear_tables_stupid()

    bertie_uuid = create_user("bertie", "hashed", "email@gmail.com")
    lottie_uuid = create_user("lottie", "hashed", "email@gmail.com")

    server = create_server("server")
    join_server(server, bertie_uuid)
    join_server(server, lottie_uuid)
    
    b_msg = send_server_message(server, bertie_uuid, "test")
    l_msg = send_server_message(server, lottie_uuid, "test")
    comb_msgs = view_server_messages(server, 100)
    print(comb_msgs)
    
    modify_server_message(server, l_msg, "new test")
    comb_msgs = view_server_messages(server, 100)
    print(comb_msgs)
    
    delete_server_message(server, b_msg)
    comb_msgs = view_server_messages(server, 100)
    print(comb_msgs)

user_tester()
server_tester()