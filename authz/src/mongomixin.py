from authlib.common.encoding import json_loads, json_dumps
from authlib.oauth2.rfc6749 import ClientMixin, TokenMixin, AuthorizationCodeMixin
from authlib.oauth2.rfc6749.util import scope_to_list, list_to_scope
import time

class Oauth2ClientMixin(ClientMixin):
    "client mixin definition"
    def __init__(self, info : dict):
        self.client_id: str = info['_id']
        self.client_secret: str = info['client_secret']
        self.client_id_issued_at: int = info['client_id_issued_at']
        self.client_secret_expires_at: int = info['client_secret_expires_at']
        self._client_metadata = info['client_metadata']

    #based on requiremnets for the client mixin from authlib
    @property
    def client_info(self):
        return dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            client_id_issued_at=self.client_id_issued_at,
            client_secret_expires_at=self.client_secret_expires_at,
            )
    @property
    def client_metadata(self):
        if 'client_metadata' in self.__dict__:
            return self.__dict__['client_metadata']
        if self._client_metadata:
            data = self._client_metadata.replace("'", "\"")
            data = json_loads(data)
            self.__dict__['client_metadata'] = data
            return data
        return {}

    def set_client_metadata(self, value):
        self._client_metadata = json_dumps(value)

    @property
    def redirect_uris(self):
        return self.client_metadata.get('redirect_uris', [])

    @property
    def token_endpoint_auth_method(self):
        return self.client_metadata.get(
            'token_endpoint_auth_method',
            'client_secret_basic'
        )

    @property
    def grant_types(self):
        return self.client_metadata.get('grant_types', [])

    @property
    def response_types(self):
        return self.client_metadata.get('response_types', [])

    @property
    def client_name(self):
        return self.client_metadata.get('client_name')

    @property
    def client_uri(self):
        return self.client_metadata.get('client_uri')

    @property
    def logo_uri(self):
        return self.client_metadata.get('logo_uri')

    @property
    def scope(self):
        return self.client_metadata.get('scope')

    @property
    def contacts(self):
        return self.client_metadata.get('contacts', [])

    @property
    def tos_uri(self):
        return self.client_metadata.get('tos_uri')

    @property
    def policy_uri(self):
        return self.client_metadata.get('policy_uri')

    @property
    def jwks_uri(self):
        return self.client_metadata.get('jwks_uri')

    @property
    def jwks(self):
        return self.client_metadata.get('jwks', [])

    @property
    def software_id(self):
        return self.client_metadata.get('software_id')

    @property
    def software_version(self):
        return self.client_metadata.get('software_version')

    def get_client_id(self):
        return self.client_id

    def get_default_redirect_uri(self):
        if self.redirect_uris:
            return self.redirect_uris[0]

    def get_allowed_scope(self, scope):
        if not scope:
            return ''
        allowed = set(self.scope.split())
        scopes = scope_to_list(scope)
        return list_to_scope([s for s in scopes if s in allowed])

    def check_redirect_uri(self, redirect_uri):
        return redirect_uri in self.redirect_uris

    def has_client_secret(self):
        return bool(self.client_secret)

    def check_client_secret(self, client_secret):
        return self.client_secret == client_secret

    def check_token_endpoint_auth_method(self, method):
        return self.token_endpoint_auth_method == method

    def check_response_type(self, response_type):
        return response_type in self.response_types

    def check_grant_type(self, grant_type):
        return grant_type in self.grant_types


class Oauth2AuthorizationCodeMixin(AuthorizationCodeMixin):
    def __init__(self, info: dict):
        self.code:str=info["_id"]
        self.client_id:str=info["client_id"]
        self.redirect_uri:str=info["redirect_uri"]
        self.response_type:str=info["response_type"]
        self.scope:str=info["scope"]
        self.nonce:str=info["nonce"]
        self.auth_time:int=info["auth_time"]

    def is_expired(self):
        return self.auth_time + 300 < time.time()

    def get_redirect_uri(self):
        return self.redirect_uri

    def get_scope(self):
        return self.scope

    def get_auth_time(self):
        return self.auth_time

    def get_nonce(self):
        return self.nonce

    def get_code(self):
        return self.code

class Oauth2TokenMixin(TokenMixin):
    def __init__(self, info: dict):
        self.id:str=info["_id"]
        self.client_id:str=info["client_id"]
        self.user_id:str=info["user_id"]
        self.token_type:str=info["token_type"]
        self.access_token:str=info["access_token"]
        self.scope:str=info["scope"]
        self.issued_at:int=info["issued_at"]
        self.access_token_revoked_at:int=info["access_token_revoked_at"]
        self.expires_in:int=info["expires_in"]

    def check_client(self, client):
        return self.client_id == client.get_client_id()

    def get_scope(self):
        return self.scope

    def get_expires_in(self):
        return self.expires_in

    def get_expires_at(self):
                return self.issued_at + self.expires_in

    def is_revoked(self):
        return self.access_token_revoked_at

    def is_expired(self):
        if not self.expires_in:
            return False

        expires_at = self.issued_at + self.expires_in
        return expires_at < time.time()