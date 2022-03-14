from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from typing import List
import motor.motor_asyncio

from model import UserModel, UpdateUserModel, ClientModel, UpdateClientModel, TokenModel

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:example@mongo:27017/?authSource=admin")
db = client.authn

@app.post("/user/create", response_description="Add new user", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    user = await db["users"].find_one({"sub": user["sub"]})
    if not user:
        new_user = await db["users"].insert_one(user)
        created_user = await db['users'].find_one({"_id": new_user.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)

@app.get('/user/list', response_description="List all users", response_model=List[UserModel])
async def list_users():
    users = await db["users"].find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)

@app.get("/user/{sub}", response_description="Get a user", response_model=UserModel)
async def list_users(sub: str):
    user = await db["users"].find_one({"sub": sub})
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No user found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)

@app.post('/user/delete', response_description="delete a user", response_model=UserModel)
async def delete_user(user: UserModel = Body(...)):
    current_user = await db["users"].find_one({"sub": user["sub"]})
    if current_user is not None:
        res = await db["users"].deleteOne({"sub": user["sub"]})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "user not found"})
    if res.deletedCount >= 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "true"})
    else:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED)  

@app.put("/user/update/{id}", response_model= UserModel, response_description="update a users info")
async def update_user(id: str, user : UpdateUserModel = Body(...)):
    user = {key: value for key, value in user.dict().items() if value is not None}
    if len(user) >= 1:
        update_result = await db["users"].update_one({"_id": id}, {"$set": user})
        if update_result.modified_count == 1:
            if (updated_user := await db["users"].find_one({"_id": id})) is not None:
                return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=updated_user)
    if (existing_user := await db["users"].find_one({"_id": id})) is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=existing_user)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

@app.post("/client/create", response_description="Add new client", response_model=ClientModel)
async def create_client(client: ClientModel = Body(...)):
    client = jsonable_encoder(client)
    client = await db["clients"].find_one({"sub": client["sub"]})
    if not client:
        new_client = await db["clients"].insert_one(client)
        created_client = await db['clients'].find_one({"_id": new_client.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_client)
    return JSONResponse(status_code=status.HTTP_200_OK, content=client)

@app.get('/client/list', response_description="List all clients", response_model=List[ClientModel])
async def list_clients():
    clients = await db["clients"].find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=clients)

@app.get("/client/{sub}", response_description="Get a client", response_model=ClientModel)
async def list_clients(sub: str):
    client = await db["clients"].find_one({"sub": sub})
    if not client:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No client found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=client)

@app.post('/client/delete', response_description="delete a client", response_model=ClientModel)
async def delete_client(client: ClientModel = Body(...)):
    current_client = await db["clients"].find_one({"sub": client["sub"]})
    if current_client is not None:
        res = await db["clients"].deleteOne({"sub": client["sub"]})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "client not found"})
    if res.deletedCount >= 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "true"})
    else:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED)

@app.put("/client/update/{id}", response_model= ClientModel, response_description="update a client object")
async def update_client(id: str, client : UpdateClientModel = Body(...)):
    client = {key: value for key, value in client.dict().items() if value is not None}
    if len(client) >= 1:
        update_result = await db["clients"].update_one({"_id": id}, {"$set": client})
        if update_result.modified_count == 1:
            if (updated_client := await db["clients"].find_one({"_id": id})) is not None:
                return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=updated_client)
    if (existing_client := await db["clients"].find_one({"_id": id})) is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=existing_client)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

@app.post("/token/create", response_description="Add new token", response_model=TokenModel)
async def create_token(token: TokenModel = Body(...)):
    token = jsonable_encoder(token)
    token = await db["tokens"].find_one({"sub": token["sub"]})
    if not token:
        new_token = await db["tokens"].insert_one(token)
        created_token = await db['tokens'].find_one({"_id": new_token.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_token)
    return JSONResponse(status_code=status.HTTP_200_OK, content=token)

@app.get('/token/list', response_description="List all tokens", response_model=List[TokenModel])
async def list_tokens():
    tokens = await db["tokens"].find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=tokens)

@app.get("/token/{sub}", response_description="Get a token", response_model=TokenModel)
async def list_tokens(sub: str):
    token = await db["tokens"].find_one({"sub": sub})
    if not token:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No token found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=token)

@app.post('/token/delete', response_description="delete a token", response_model=TokenModel)
async def delete_token(token: TokenModel = Body(...)):
    current_token = await db["tokens"].find_one({"sub": token["sub"]})
    if current_token is not None:
        res = await db["tokens"].deleteOne({"sub": token["sub"]})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "token not found"})
    if res.deletedCount >= 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "true"})
    else:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED)
