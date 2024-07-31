from typing import Union
from fastapi import APIRouter, HTTPException,status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userDB", tags=["userDB"], responses={status.HTTP_404_NOT_FOUND: {"message":"Error"}})

#inicio de server: uvicorn main:app --reload  o fastapi dev main.py
#entidad user


#get user 


@router.get("/",response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get("/{id}")
async def userID(id: str):
    return search_user("_id",ObjectId(id))
    
def search_user(field:str, key):
    try:
       user = db_client.users.find_one({field:key})
       return User(**user_schema(user))
    except:
        return {"Error":"No existe"}
    
#post user
@router.post("/",response_model=User,status_code=201)
async def user(user : User):
    if type(search_user("correo", user.correo)) == User:
     raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuario Existente")
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id":id}))
    return User(**new_user)



#put user 
@router.put("/", response_model= User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
       db_client.users.find_one_and_replace({"_id":ObjectId(user.id)},user_dict)
    except:
     return {"Error":"Usuario no Actualizado"}

    return search_user("_id", ObjectId(user.id))
       
       
#delete user       
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def userID(id: str):
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
     return {"Error":"No encontrado"}