import requests
import json
from config import db_api_url, base_permissions
import logging

def build_user_json(user):
    json_user = {
        "uuid": f"{user['sub']}",
        "sub": f"{user['sub']}",
        "name": f"{user['name']}",
        "permissions": base_permissions
    }
    return json.dumps(json_user)

def create_json_user(user):
    create_user_endpoint = db_api_url+"/create"
    json_user = build_user_json(user)
    response = requests.post(create_user_endpoint, json=json_user)
    if response.status_code == 201:
        return True
    return False 

def user_exists(user):
    user_endpoint = db_api_url + "/user/" + str(user['sub'])
    response = requests.get(user_endpoint)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise Exception("Unknown Error as occurred")
    
def create_query_client_func(session, client_model):
    """Create an ``query_client`` function that can be used in authorization
    server.
    :param session: MongoDB session
    :param client_model: Client model class
    """
    def query_client(client_id):
        q = session.query(client_model)
        return q.filter_by(client_id=client_id).first()
    return query_client