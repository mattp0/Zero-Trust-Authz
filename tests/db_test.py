import requests
import json
import secrets
import time

debug = b'{"_id":"623e9246edbe11b44fcd2584","client_secret":"M9UEmClSSNWF0luDMnwLVgTHK4r5aIDWF35E0tEg9kk","client_id_issued_at":1648267846,"client_secret_expires_at":1648351846,"client_metadata":"{\'redirect_uris\': [\'http://localhost/auth\'],\'token_endpoint_auth_method\': \'client_secret_basic\',\'grant_types\': [\'authorization_code\'],\'response_types\': [\'code\'],\'client_name\': \'The Main Frame\',\'client_uri\': \'http://localhost\',\'scope\': \'openid profile email\'}"}'

db_api_url = "http://192.168.40.189:8070"

test_user = {
        "email": "matt@mperry.io",
        "name": "test test",
        "hd": "mperry.io",
        "permissions": ["test"]
}

test_perms = {
    "permissions": ["web"]
}

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

def create_json_user(user):
    print("testing create user")
    create_user_endpoint = db_api_url+"/user/create"
    response = requests.post(create_user_endpoint, data=json.dumps(user))
    if response.status_code == 200:
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
        "client_metadata": "{'redirect_uris': ['http://localhost/auth'],'token_endpoint_auth_method': 'client_secret_basic','grant_types': ['authorization_code'],'response_types': ['code'],'client_name': 'The Main Frame','client_uri': 'http://localhost','scope': 'openid profile email'}"
    }
    update_endpoint = db_api_url + "/client/create"
    print("preparing to send post request")
    print(json.dumps(data))
    response = requests.post(update_endpoint, data=json.dumps(data))
    print("sent post")
    if response.status_code == 202 or response.status_code == 200:
        return True, response.content
    return False, None

def create_authcode():
    data = {
        "client_id": "45123",
        "redirect_uri": "http://mperry.io",
        "response_code": "code",
        "scope": "openid profile email",
        "grant_user": "21323423245",
        "nonce": "1212134",
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

def save_token():
    item = {'client_id': '623e9246edbe11b44fcd2584', 'user_id': '623e9262edbe11b44fcd2585', 'issued_at': 1648274469, 'expires_in': 864000, 'access_token_revoked_at': 0, 'token_type': 'Bearer', 'access_token': 'ljH84ejvxqAMZ8s75eyukWxN5oWUyh6RsTmMaoUI30', 'scope': 'openid email profile'}
    client_endpoint = db_api_url + "/token/create"
    print(item)
    response = requests.post(client_endpoint, data=json.dumps(item))
    print(response.status_code)

if __name__ == "__main__":
    save_token()
    # res, user = user_exists(test_user)
    # print("testing if a user can be made twice")
    # dupe_res, dupe_user = create_json_user(test_user)
    # print(dupe_user)
    # if dupe_res:
    #     print("something failed")
    # if res:
    #     res, user = update_user(user, test_perms)
    #     print(user)
    # else:
    #     res, user = create_json_user(test_user)
    #     print(user)
    #     if res:
    #         res, user = update_user(user, test_perms)
    #         print(user)
    # print("testing client creation")
    # res, content = create_client()
    # print(res, content)
    # print("testing authcode creation")
    # res, content = create_authcode()
    # print(res, content)
    # data = json.loads(content)
    # print("get getter for authcode")
    # res, content = get_authcode(data['_id'])
    # print(res, content)
    # print(json.loads(content))

    # print("get delete for authcode")
    # res = delete_authcode(data['_id'])
    # print(res)

    # print("get getter for authcode")
    # res, content = get_authcode(data['_id'])
    # print(res, content)
    # if content is not None:
    #     print(json.loads(content))