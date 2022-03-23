from urllib import response
from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.oauth2.rfc6749.grants import (
    AuthorizationCodeGrant as _AuthorizationCodeGrant,
)
from authlib.oidc.core import UserInfo
from authlib.oidc.core.grants import OpenIDCode as _OpenIDCode
from mongomixin import Oauth2ClientMixin, Oauth2AuthorizationCodeMixin, Oauth2TokenMixin
from helper import (
    create_bearer_token_validator,
    query_client,
    save_token,
    create_authz_code,
    get_authz_code,
    delete_authz_code,

)
from model import User
import json
from mock_info import fake_user

DUMMY_JWT_CONFIG = {
    'key': 'secret-key',
    'alg': 'HS256',
    'iss': 'https://mperry.io',
    'exp': 3600,
}

def create_authorization_code(client, grant_user, request):
    data = {
        "client_id": client.client_id,
        "redirect_uri": request.redirect_url,
        "scope": request.scope,
        "grant_user": grant_user.id,
        "nonce": request.data.get('nonce')
    }
    info = json.loads(create_authz_code(data))
    item = Oauth2AuthorizationCodeMixin(info)
    return item.get_code()

class AuthorizationCodeGrant(_AuthorizationCodeGrant):
    def create_authorization_code(self, client, grant_user, request):
        return create_authorization_code(client, grant_user, request)

    def parse_authorization_code(self, code, client):
        info = json.loads(get_authz_code(code))
        item = Oauth2AuthorizationCodeMixin(info)
        if item and not item.is_expired():
            return item

    def delete_authorization_code(self, authorization_code):
        res = delete_authz_code(authorization_code)

    def authenticate_user(self, authorization_code):
        info = json.loads(get_authz_code(authorization_code))
        
        user = User(fake_user)
        return user

def exists_nonce(nonce, req):
    return True

def generate_user_info(user, scope):
    print(user)
    return UserInfo(name=user.get_name(), email=user.get_email(), team="web")

class OpenIDCode(_OpenIDCode):
    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self, grant):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user, scope)


authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token,
)
require_oauth = ResourceProtector()


def config_oauth(app):
    authorization.init_app(app)

    authorization.register_grant(AuthorizationCodeGrant, [
        OpenIDCode(require_nonce=False),
    ])


    # protect resource
    bearer_cls = create_bearer_token_validator()
    require_oauth.register_token_validator(bearer_cls())