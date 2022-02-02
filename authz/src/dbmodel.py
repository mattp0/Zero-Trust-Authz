from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
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
                "client_id": "1231231231",
                "client_secret": "joe bob",
                "client_id_issued_at": 45123,
                "client_secret_expires_at": 84000,
                "_client_metadata": ["web", "admin", "chat"],
            }
        }
