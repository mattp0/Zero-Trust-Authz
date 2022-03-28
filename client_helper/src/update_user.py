import secrets
import json
import requests
import time
db_api_url = "http://authz-dbapi"
new_perms = {
    "permissions": ["web"]
}


def update_user(user, new_user):
    print(f"testing update user, with info:{user}, to {new_user}")
    update_endpoint = db_api_url + "/user/update/" + user["_id"]
    response = requests.put(update_endpoint, data=json.dumps(new_user))
    if response.status_code == 200:
        return True
    return False

def user_exists(user):
    print("testing user exists")
    user_endpoint = db_api_url + "/user/" + str(user['email'])
    response = requests.get(user_endpoint)
    if response.status_code == 200:
        return True, response.content
    elif response.status_code == 404:
        return False, None
    else:
        raise Exception("Unknown Error as occurred")

if __name__ == "__main__":
    user = {"email": "mperry37@alaska.edu"}
    res, content = user_exists(user)
    user_info = json.loads(content)
    res = update_user(user_info, new_perms)
    print(res)
    