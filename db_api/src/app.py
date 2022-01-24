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

@app.post("/create", response_description="Add new user", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    user = await db["collection"].find_one({"sub": user["sub"]})
    if not user:
        new_user = await db["collection"].insert_one(user)
        created_user = await db['collection'].find_one({"_id": new_user.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)

@app.get('/users', response_description="List all users", response_model=List[UserModel])
async def list_users():
    users = await db["collection"].find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)

@app.get("/user/{sub}", response_description="Get a user", response_model=UserModel)
async def list_users(sub: str):
    user = await db["collection"].find_one({"sub": sub})
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No user found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)

@app.post('/delete', response_description="delete a user", response_model=UserModel)
async def delete_user(user: UserModel = Body(...)):
    current_user = await db["collection"].find_one({"sub": user["sub"]})
    if current_user is not None:
        res = await db["collection"].deleteOne({"sub": user["sub"]})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "user not found"})
    if res.deletedCount >= 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "true"})
    else:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED)  

@app.put("/update/{id}", response_model= UserModel, response_description="update a users info")
async def update_user(id: str, user : UpdateUserModel = Body(...)):
    user = {key: value for key, value in user.dict().items() if value is not None}
    if len(user) >= 1:
        update_result = await db["collection"].update_one({"_id": id}, {"$set": user})
        if update_result.modified_count == 1:
            if (updated_user := await db["collection"].find_one({"_id": id})) is not None:
                return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=updated_user)
    if (existing_user := await db["collection"].find_one({"_id": id})) is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=existing_user)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
