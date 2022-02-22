import requests
import json
from config import db_api_url, base_permissions
import logging
import time
from mongomixin import Oauth2ClientMixin, Oauth2AuthorizationCodeMixin, Oauth2TokenMixin
from mock_info import client_info, meta, token_info

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
        print(response.status_code)
        raise Exception("Unknown Error as occurred")


def query_client(client_id):
    #query dbapi by the client id
    print("querying the client!")
    client = Oauth2ClientMixin(client_info, meta)
    print(client.client_id, client_id)
    return client
  
def save_token(token_data, request):
    if request.user:
        user_id = request.user.get_user_id()
    else:
        user_id = None
    client = request.client
    #parse token into api call
    item ={
        "client_id":client.client_id,
        "user_id":user_id,
        "token":token_data,
    }
    token = (item)
    print("looking to save the token!")
    print(token)
    #TODO add mongo API call to save token!
  


def create_query_token_func():
    """Create an ``query_token`` function for revocation, introspection
    token endpoints.
    """
    def query_token(token, token_type_hint):
        print("we are looking for tokens?")
        if token_type_hint == 'access_token':
            return True # need to define a db api call to look at token by access
        elif token_type_hint == 'refresh_token':
            return True # need to define a db api call to look at token by refresh
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
            print("creating a token")
            token = Oauth2TokenMixin()
            print(token)
            print(token_string)
            return token

        def request_invalid(self, request):
            return False

        def token_revoked(self, token):
            return token.revoked

    return _BearerTokenValidator