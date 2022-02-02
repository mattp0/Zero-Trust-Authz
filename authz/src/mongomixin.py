from authlib.common.encoding import json_loads, json_dumps
from authlib.oauth2.rfc6749 import ClientMixin
from authlib.oauth2.rfc6749 import scope_to_list, list_to_scope
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Dict, List
import secrets

class ClientObject(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid Object")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ClientMetadata(BaseModel):
    redirect_uris: List[str]
    token_endpoint_auth_method: str
    client_secret_basic: str
    grant_types: List[str]
    response_types: List[str]
    client_name: str
    client_uri: str
    logo_uri: str
    scope: str
    contacts: List[str]
    tos_uri: str
    policy_uri: str
    jwks_uri: str
    jwks: List[str]
    software_id: str
    software_version: str
    


class MongoClientMixin(ClientMixin, BaseModel):
    client_id: ClientObject = Field(default_factory=ClientObject, alias="_id")
    client_secret: str = Field(...)
    client_id_issued_at: int = Field(...)
    client_secret_expires_at: int = Field(...)
    _client_metadata: ClientMetadata = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "client_id": "1231231231",
                "client_secret": "joe bob",
                "client_id_issued_at": 45123,
                "client_secret_expires_at": 84000,
                "_client_metadata": ["web", "admin", "chat"],
            }
        }
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
        if self._client_metadata:
            return self._client_metadata
        return None
    @property
    def client_metadata(self):
        if 'client_metadata' in self.__dict__:
            return self.__dict__['client_metadata']
        if self._client_metadata:
            data = json_loads(self._client_metadata)
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
        return self.client_metadata.get('scope', '')

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

    def check_endpoint_auth_method(self, method, endpoint):
        if endpoint == 'token':
            return self.token_endpoint_auth_method == method
        # TODO
        return True

    def check_response_type(self, response_type):
        return response_type in self.response_types

    def check_grant_type(self, grant_type):
        return grant_type in self.grant_types
