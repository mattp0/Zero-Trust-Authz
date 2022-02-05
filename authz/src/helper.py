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
            return token_string

        def request_invalid(self, request):
            return False

        def token_revoked(self, token):
            return token.revoked

    return _BearerTokenValidator