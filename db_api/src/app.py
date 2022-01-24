from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from typing import List
import motor.motor_asyncio

from model import UserModel, UpdateUserModel

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:example@mongo:27017/?authSource=admin")
db = client.authn

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
    uuid: UserObject = Field(default_factory=UserObject, alias="_uuid")
    name: str = Field(...)
    permissions: List[str] = Field(...)

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "uuid": "12312421212",
                "name": "joe bob",
                "permissions": ["web", "admin", "chat"],
            }
        }

class UpdateUserModel(BaseModel):
    uuid: Optional[str]
    name: Optional[str]
    permissions: Optional[List[str]]

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "uuid": "12312421212",
                "name": "joe bob",
                "permissions": ["web", "admin", "chat"],
            }
        }


@app.post("/create", response_description="Add new user", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db["collection"].insert_one(user)
    created_user = await db["collection"].find_one({"uuid": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

@app.get('/users', response_description="List all users", response_model=List[UserModel])
async def list_users():
    users = await db["collection"].find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)

@app.get('/user', response_description="Get a user", response_model=UserModel)
async def list_users(user: UserModel = Body(...)):
    user = await db["collection"].find_one({"uuid": user})
    if not user:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)

@app.post('/delete', response_description="delete a user", response_model=UserModel)
async def delete_user(user: UserModel = Body(...)):
    current_user = await db["collection"].find_one({"uuid": user.uuid})
    if current_user is not None:
        res = await db["collection"].deleteOne({"uuid": user.uuid})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "user not found"})
    if res.deletedCount >= 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "true"})
    else:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED, content={"error": "did not delete user"})  
