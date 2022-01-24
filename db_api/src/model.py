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