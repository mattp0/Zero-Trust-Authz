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
        return False      return False 
