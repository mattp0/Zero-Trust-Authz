import secrets
import json
import requests
import time
db_api_url = "http://authz-dbapi"

def create_client():
    data = {
        "client_secret": secrets.token_urlsafe(32),
        "client_id_issued_at": int(time.time()),
        "client_secret_expires_at": int(time.time()) + int(84_000),
        "client_metadata": "{'redirect_uris': ['http://secret.mperry.io/auth'],'token_endpoint_auth_method': 'client_secret_basic','grant_types': ['authorization_code'],'response_types': ['code'],'client_name': 'The Main Frame','client_uri': 'http://secret.mperry.io','scope': 'openid profile email'}"
    }
    update_endpoint = db_api_url + "/client/create"
    print("preparing to send post request")
    print(json.dumps(data))
    response = requests.post(update_endpoint, data=json.dumps(data))
    if response.status_code == 202 or response.status_code == 200:
        return True, response.content
    return False, None


if __name__ == "__main__":
    print("Creating a client")
    res, content = create_client()
    print(res, content)
    