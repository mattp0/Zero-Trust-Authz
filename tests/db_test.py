import requests
import json

db_api_url = "http://172.23.144.1:8070"

test_user = {
        "sub": "1057831111111",
        "name": "test test",
        "permissions": ["test"]
}

test_perms = {
    "permissions": ["admin"]
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
    create_user_endpoint = db_api_url+"/create"
    response = requests.post(create_user_endpoint, data=user)
    if response.status_code == 201:
        print(response.content)
        return True, response.content
    return False, None 

def update_user(user, new_user):
    print(f"testing update user, with info:{user}, to {new_user}")
    user = json.loads(str(user, "utf-8"))
    update_endpoint = db_api_url + "/update/" + user["_id"]
    response = requests.put(update_endpoint, data=json.dumps(new_user))
    if response.status_code == 202 or response.status_code == 200:
        return True, response.content
    return False, None

if __name__ == "__main__":
    res, user = user_exists(test_user)
    print("testing if a user can be made twice")
    dupe_res, dupe_user = create_json_user(json.dumps(test_user))
    if dupe_res:
        print("something failed")
    if res:
        res, user = update_user(user, test_perms)
        print(user)
    else:
        res, user = create_json_user(json.dumps(test_user))
        if res:
            res, user = update_user(user, test_perms)
            print(user)
