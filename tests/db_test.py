import requests
import json
import secrets
import time

db_api_url = "http://192.168.40.189:8070"

test_user = {
        "sub": "1057831111111",
        "name": "test test",
        "permissions": ["test"]
}

test_perms = {
    "permissions": ["web"]
}

def user_exists(user):
    print("testing user exists")
    user_endpoint = db_api_url + "/user/" + str(user['sub'])
    response = requests.get(user_endpoint)
    if response.status_code == 200:
        return True, response.content
    elif response.status_code == 404:
        return False, None
    else:
        raise Exception("Unknown Error as occurred")

def create_json_user(user):
    print("testing create user")
    create_user_endpoint = db_api_url+"/user/create"
    response = requests.post(create_user_endpoint, data=json.dumps(user))
    if response.status_code == 201:
        print(response.content)
        return True, response.content
    return False, None 

def update_user(user, new_user):
    print(f"testing update user, with info:{user}, to {new_user}")
    user = json.loads(str(user, "utf-8"))
    update_endpoint = db_api_url + "/user/update/" + user["_id"]
    response = requests.put(update_endpoint, data=json.dumps(new_user))
    if response.status_code == 202 or response.status_code == 200:
        return True, response.content
    return False, None

def create_client():
    data = {
        "client_secret": secrets.token_urlsafe(32),
        "client_id_issued_at": int(time.time()),
        "client_secret_expires_at": int(time.time()) + int(84_000),
        "_client_metadata": ["made by a test"]
    }
    update_endpoint = db_api_url + "/client/create"
    print("preparing to send post request")
    response = requests.post(update_endpoint, data=json.dumps(data))
    print("sent post")
    if response.status_code == 202 or response.status_code == 200:
        return True, response.content
    return False, None

def create_authcode():
    data = {
        "client_id": "45123",
        "redirect_uri": "http://mperry.io",
        "scope": "openid profile email",
        "grant_user": "21323423245",
        "nonce": "1212134"
    }
    update_endpoint = db_api_url + "/authcode/create"
    response = requests.post(update_endpoint, data=json.dumps(data))
    if response.status_code == 202 or response.status_code == 200:
        return True, response.content
    return False, None

def get_authcode(code):
    update_endpoint = db_api_url + "/authcode/" + code
    response = requests.get(update_endpoint)
    if response.status_code == 200:
        return True, response.content
    return False, None

def delete_authcode(code):
    update_endpoint = db_api_url + "/authcode/delete/" + code
    response = requests.get(update_endpoint)
    if response.status_code == 200:
        return True
    return False

if __name__ == "__main__":
    res, user = user_exists(test_user)
    print("testing if a user can be made twice")
    dupe_res, dupe_user = create_json_user(test_user)
    print(dupe_user)
    if dupe_res:
        print("something failed")
    if res:
        res, user = update_user(user, test_perms)
        print(user)
    else:
        res, user = create_json_user(test_user)
        print(user)
        if res:
            res, user = update_user(user, test_perms)
            print(user)
    print("testing client creation")
    res, content = create_client()
    print(res, content)
    print("testing authcode creation")
    res, content = create_authcode()
    print(res, content)
    data = json.loads(content)
    print("get getter for authcode")
    res, content = get_authcode(data['_id'])
    print(res, content)
    print(json.loads(content))

    print("get delete for authcode")
    res = delete_authcode(data['_id'])
    print(res)

    print("get getter for authcode")
    res, content = get_authcode(data['_id'])
    print(res, content)
    if content is not None:
        print(json.loads(content))