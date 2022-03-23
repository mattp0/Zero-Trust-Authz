from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List

class UserObject(ObjectId):
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

class UserModel(BaseModel):
    id: UserObject = Field(default_factory=UserObject, alias="_id")
    sub: str = Field(...)
    name: str = Field(...)
    permissions: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "sub": "1231231231",
                "name": "joe bob",
                "permissions": ["web", "admin", "chat"],
            }
        }

class UpdateUserModel(BaseModel):
    sub: Optional[str]
    name: Optional[str]
    permissions: Optional[List[str]]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "sub": "1231231231",
                "name": "joe bob",
                "permissions": ["web", "admin", "chat"],
            }
        }

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

class ClientModel(BaseModel):
    client_id: ClientObject = Field(default_factory=ClientObject, alias="_id")
    client_secret: str = Field(...)
    client_id_issued_at: int = Field(...)
    client_secret_expires_at: int = Field(...)
    _client_metadata: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "client_secret": "joe bob",
                "client_id_issued_at": 45123,
                "client_secret_expires_at": 84000,
                "_client_metadata": ["web", "admin", "chat"],
            }
        }

class TokenObject(ObjectId):
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

class TokenModel(BaseModel):
    id: TokenObject = Field(default_factory=TokenObject, alias="_id")
    token_id: str = Field(...)
    token_type: str = Field(...)
    scope: str = Field(...)
    access_token: str = Field(...)
    expires_in: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "token_id": "sadfasdfasdfwerdadf21342wsfda",
                "token_type": "Bearer",
                "scope": "openid profile email",
                "access_token": 'swerasdfwewdasdf',
                "expires_in": 84000,
            }
        }

class AuthCodeObject(ObjectId):
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

class AuthCodeModel(BaseModel):
    code: AuthCodeObject = Field(default_factory=AuthCodeObject, alias="_id")
    client_id: str = Field(...)
    redirect_uri: str = Field(...)
    scope: str = Field(...)
    grant_user: str = Field(...)
    nonce : str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "client_id": "45123",
                "redirect_uri": "http://mperry.io",
                "scope": "openid profile email",
                "grant_user": "21323423245",
                "nonce": "1212134"
            }
        }