from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI
from typing import List
import motor.motor_asyncio

from model import UserModel, UpdateUserModel, ClientModel, AuthCodeModel, TokenModel

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:example@authz-mongo:27017/?authSource=admin")
db = client.authn
mongo_users = db['users']
mongo_clients = db['clients']
mongo_tokens = db['tokens']
mongo_authcodes = db['authcodes']
@app.post("/user/create", response_description="Add new user", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await mongo_users.insert_one(user)
    created_user = await db['users'].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=created_user)

@app.get('/user/list', response_description="List all users", response_model=List[UserModel])
async def list_users():
    users = await mongo_users.find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)

@app.get("/user/{sub}", response_description="Get a user", response_model=UserModel)
async def get_user(sub: str):
    user = await mongo_users.find_one({"sub": sub})
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No user found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)

@app.post('/user/delete', response_description="delete a user", response_model=UserModel)
async def delete_user(user: UserModel = Body(...)):
    res = await mongo_users.delete_one({"sub": user["sub"]})
    if res.deleted_count >= 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "true"})
    else:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED)  

@app.put("/user/update/{id}", response_model= UserModel, response_description="update a users info")
async def update_user(id: str, user : UpdateUserModel = Body(...)):
    user = {key: value for key, value in user.dict().items() if value is not None}
    if len(user) >= 1:
        update_result = await mongo_users.update_one({"_id": id}, {"$set": user})
        if update_result.modified_count == 1:
            if (updated_user := await mongo_users.find_one({"_id": id})) is not None:
                return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=updated_user)
    if (existing_user := await mongo_users.find_one({"_id": id})) is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=existing_user)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

@app.post("/client/create", response_description="Add new client", response_model=ClientModel)
async def create_client(client: ClientModel = Body(...)):
    client = jsonable_encoder(client)
    new_client = await mongo_clients.insert_one(client)
    created_client = await db['clients'].find_one({"_id": new_client.inserted_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=created_client)

@app.get("/client/{id}", response_description="Get a client", response_model=ClientModel)
async def get_client(id: str):
    client = await mongo_clients.find_one({"_id": id})
    if not client:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No client found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=client)

@app.post('/client/delete', response_description="delete a client", response_model=ClientModel)
async def delete_client(client: ClientModel = Body(...)):
    res = await mongo_clients.delete_one({"sub": client["sub"]})
    if res.deleted_count >= 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "true"})
    else:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED)  

@app.post("/token/create", response_description="Add new token", response_model=TokenModel)
async def create_token(token: TokenModel = Body(...)):
    token = jsonable_encoder(token)
    new_token = await mongo_tokens.insert_one(token)
    created_token = await db['tokens'].find_one({"_id": new_token.inserted_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=created_token)

@app.get("/token/{token_str}", response_description="Get a token", response_model=TokenModel)
async def get_token(token_str: str):
    token = await mongo_tokens.find_one({"token_id": token_str})
    if not token:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="No token found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=token)

@app.post('/token/delete', response_description="delete a token", response_model=TokenModel)
async def delete_token(token: TokenModel = Body(...)):
    res = await mongo_tokens.delete_one({"token_id": token["token_id"]})
    if res.deleted_count >= 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "true"})
    else:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED)  

@app.post("/authcode/create", response_description="Add new authcode", response_model=AuthCodeModel)
async def create_authcode(authcode: AuthCodeModel = Body(...)):
    authcode = jsonable_encoder(authcode)
    new_authcode = await mongo_authcodes.insert_one(authcode)
    created_authcode = await db['authcodes'].find_one({"_id": new_authcode.inserted_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=created_authcode)

@app.get("/authcode/{code}", response_description="Get a authcode", response_model=AuthCodeModel)
async def get_authcode(code: str):
    authcode = await mongo_authcodes.find_one({"_id": code})
    if not authcode:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="No token found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=authcode)

@app.get('/authcode/delete/{authcode}', response_description="delete a authcode")
async def delete_authcode(authcode: str):
    res = await mongo_authcodes.delete_one({"_id": authcode})
    if res.deleted_count >= 1:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"success": "true"})
    else:
        return JSONResponse(status_code=status.HTTP_304_NOT_MODIFIED)  