from pydantic import BaseModel, Field
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
    email: str = Field(...)
    name: str = Field(...)
    hd: str = Field(...)
    permissions: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "mperry37@alaska.edu",
                "name": "joe bob",
                "hd": "mperry.io",
                "permissions": ["web", "admin", "chat"],
            }
        }

class UpdateUserModel(BaseModel):
    email: Optional[str]
    name: Optional[str]
    hd: Optional[str]
    permissions: Optional[List[str]]
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "mperry37@alaska.edu",
                "name": "joe bob",
                "hd": "mperry.io",
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
    client_metadata: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "client_secret": "joe bob",
                "client_id_issued_at": 45123,
                "client_secret_expires_at": 84000,
                "client_metadata": "stuff",
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
    client_id: str = Field(...)
    user_id: str = Field(...)
    token_type: str = Field(...)
    scope: str = Field(...)
    access_token: str = Field(...)
    expires_in: int = Field(...)
    issued_at: int = Field(...)
    access_token_revoked_at: int = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "client_id": "1231232145",
                "user_id": "1231232",
                "token_type": "Bearer",
                "access_token": 'swerasdfwewdasdf',
                "scope": "openid profile email",
                "issued_at": 12314,
                "access_token_revoked_at": 123124,
                "expires_in": 0,
            }
        }

class UpdateTokenModel(BaseModel):
    client_id: Optional[str] 
    user_id: Optional[str] 
    token_type: Optional[str] 
    scope: Optional[str] 
    access_token: Optional[str] 
    expires_in: Optional[int] 
    issued_at: Optional[int] 
    access_token_revoked_at: Optional[int] 
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "client_id": "1231232145",
                "user_id": "1231232",
                "token_type": "Bearer",
                "access_token": 'swerasdfwewdasdf',
                "scope": "openid profile email",
                "issued_at": 12314,
                "access_token_revoked_at": 123124,
                "expires_in": 0,
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
    response_type: str = Field(...)
    scope: str = Field(...)
    grant_user: str = Field(...)
    nonce : str = Field(...)
    auth_time: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "client_id": "45123",
                "redirect_uri": "http://mperry.io",
                "response_type": "code",
                "scope": "openid profile email",
                "grant_user": "21323423245",
                "nonce": "1212134",
                "auth_time": 12314512312
            }
        }