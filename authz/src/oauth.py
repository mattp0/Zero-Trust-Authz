from authlib.integrations.flask_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
)
from authlib.oauth2.rfc6749.grants import (
    AuthorizationCodeGrant as _AuthorizationCodeGrant,
)
from authlib.oidc.core import UserInfo
from authlib.oidc.core.grants import OpenIDCode as _OpenIDCode
from mongomixin import Oauth2AuthorizationCodeMixin
from helper import (
    create_bearer_token_validator,
    query_client,
    save_token,
    create_authz_code,
    get_authz_code,
    delete_authz_code,
    get_user_by_id,
    create_revocation_endpoint

)
from model import User
import json
import secrets
import time
from config import DUMMY_JWT_CONFIG, allowed_permission

def create_authorization_code(client, grant_user, request):
    data = {
        "client_id": client.client_id,
        "redirect_uri": request.redirect_uri,
        "response_type":request.response_type,
        "scope": request.scope,
        "grant_user": grant_user.id,
        "nonce": secrets.token_urlsafe(16),
        "auth_time": int(time.time())
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
        res = delete_authz_code(authorization_code.get_code())

    def authenticate_user(self, authorization_code):
        info = json.loads(get_authz_code(authorization_code.get_code()))
        user_data = get_user_by_id(info['grant_user'])
        user = User(json.loads(user_data))
        return user

def exists_nonce(nonce, req):
    return True

def generate_user_info(user, scope):
    token_user = get_user_by_id(user)
    token_user = User(json.loads(token_user))
    permissions = token_user.get_permissions()
    if allowed_permission not in permissions:
        return UserInfo(name=token_user.get_name(), email="bad@bad.com", team="bad")
    id_email = token_user.get_user_id() + "@mperry.io"
    return UserInfo(name=token_user.get_name(), email=id_email, team=token_user.get_permissions)

class OpenIDCode(_OpenIDCode):
    def exists_nonce(self, nonce, request):
        return exists_nonce(nonce, request)

    def get_jwt_config(self, grant):
        return DUMMY_JWT_CONFIG

    def generate_user_info(self, user, scope):
        return generate_user_info(user.get_user_id(), scope)


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

    revocation_cls = create_revocation_endpoint()
    authorization.register_endpoint(revocation_cls)
    # protect resource
    bearer_cls = create_bearer_token_validator()
    require_oauth.register_token_validator(bearer_cls())