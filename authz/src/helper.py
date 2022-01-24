import requests
def build_user(user):
    return user

def build_user_json(user):
    json_user = {
        "uuid": f"{user['sub']}",
        "sub": f"{user['sub']}",
        "name": f"{user['name']}",
        "permissions": base_permissions
    }
    return json.dumps(json_user)

def create_json_user(user):
    x = requests.post(full, data=user)
    if x.status_code == 200:
        return True
    else:
        return False  