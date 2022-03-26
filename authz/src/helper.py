import requests
import json
from config import db_api_url, base_permissions, domain
import logging
import time
from mongomixin import Oauth2ClientMixin, Oauth2AuthorizationCodeMixin, Oauth2TokenMixin
from mock_info import client_info, meta, token_info

def build_user_json(user):
    json_user = {
        "email": f"{user['email']}",
        "name": f"{user['name']}",
        "hd": domain, 
        "permissions": base_permissions
    }
    return json_user

def create_json_user(user) -> dict:
    create_user_endpoint = db_api_url+"/user/create"
    json_user = build_user_json(user)
    response = requests.post(create_user_endpoint, data=json.dumps(json_user))
    if response.status_code == 200:
        return response.content
    return None

def user_exists(user) -> dict:
    user_endpoint = db_api_url + "/user/" + str(user['email'])
    response = requests.get(user_endpoint)
    if response.status_code == 200:
        return response.content
    elif response.status_code == 404:
        return None
    else:
        raise Exception("Unknown Error as occurred")

def get_user_by_id(id) -> dict:
    user_endpoint = db_api_url + "/user/id/" + id
    response = requests.get(user_endpoint)
    if response.status_code == 200:
        return response.content
    elif response.status_code == 404:
        return None
    else:
        raise Exception("Unknown Error as occurred")

def create_authz_code(data):
    update_endpoint = db_api_url + "/authcode/create"
    response = requests.post(update_endpoint, data=json.dumps(data))
    if response.status_code == 200:
        return response.content
    return None

def get_authz_code(code):
    update_endpoint = db_api_url + "/authcode/" + code
    response = requests.get(update_endpoint)
    if response.status_code == 200:
        return response.content
    return None

def delete_authz_code(code):
    update_endpoint = db_api_url + "/authcode/delete/" + code
    response = requests.get(update_endpoint)
    if response.status_code == 200:
        return True
    return False

def query_client(client_id):
    client_endpoint = db_api_url + "/client/" + str(client_id)
    response = requests.get(client_endpoint)
    client = Oauth2ClientMixin(json.loads(response.content))
    return client
  
def save_token(token, request):
    client_endpoint = db_api_url + "/token/create"
    if request.user:
        user_id = request.user.get_user_id()
    else:
        user_id = None
    client = request.client

    item ={
        "client_id": client.client_id,
        "user_id": user_id,
        "issued_at": int(time.time()),
        "expires_in": 300,
        "access_token_revoked_at": 0,
        **token
    }
    response = requests.post(client_endpoint, data=json.dumps(item))
    print(response.status_code)
    #TODO add mongo API call to save token!
  


def create_query_token_func():
    """Create an ``query_token`` function for revocation, introspection
    token endpoints.
    """
    def query_token(token, token_type_hint):
        client_endpoint = db_api_url + "/token/" + token
        response = requests.get(client_endpoint)
        return Oauth2TokenMixin(json.loads(response.content))
    return query_token


def create_revocation_endpoint():
    """Create a revocation endpoint class
    """
    from authlib.oauth2.rfc7009 import RevocationEndpoint
    query_token = create_query_token_func()

    class _RevocationEndpoint(RevocationEndpoint):
        def query_token(self, token, token_type_hint):
            return query_token(token, token_type_hint)

        def revoke_token(self, token, request):
            now = int(time.time())
            hint = request.form.get('token_type_hint')
            token.access_token_revoked_at = now
            if hint != 'access_token':
                token.refresh_token_revoked_at = now
            #write token to db api

    return _RevocationEndpoint


def create_bearer_token_validator():
    """Create an bearer token validator class
    """
    from authlib.oauth2.rfc6750 import BearerTokenValidator

    class _BearerTokenValidator(BearerTokenValidator):
        def authenticate_token(self, token_string):
            #search for token in db api call. returns the token
            client_endpoint = db_api_url + "/token/" + token_string
            response = requests.get(client_endpoint)
            return Oauth2TokenMixin(json.loads(response.content))

        def request_invalid(self, request):
            return False

        def token_revoked(self, token):
            revoke_time = token.is_revoked()
            if revoke_time != 0:
                if revoke_time > int(time.time()):
                    return True
            return False

    return _BearerTokenValidator