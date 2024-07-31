from typing import Union

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter(prefix="/user", tags=["user"], responses={404: {"message":"Error"}})

#inicio de server: uvicorn main:app --reload  o fastapi dev main.py
#entidad user

class User(BaseModel):
    id:int
    nombre: str
    apellidoP:str
    apellidoM:str
    edad: int

user_List = [User(id=1, nombre="Anthony",apellidoP="Aldunate",apellidoM="Justiniano",edad=26),
         User(id=2, nombre= "Majo",apellidoP ="Pereira",apellidoM="Aliaga",edad=26),
         User(id=3, nombre="Kiara",apellidoP="Aldunate",apellidoM="Justiniano",edad=8)]

#get user 

@router.get("/")
async def usersJson():
    return [{"Nombre": "Anthony", "apellidoP":"Aldunate", "apellidoM":"Justiniano", "edad":26},
            {"Nombre": "Majo", "apellidoP":"pereira", "edad":23},
            {"Nombre": "Kiara", "apellidoP":"Aldunate", "edad":8}]

@router.get("/1")
async def user():
    return user_List


@router.get("/{id}")
async def userID(id: int):
    return search_user(id)
    
@router.get("/")
async def userID(id: int):
    return search_user(id)
    
def search_user(id:int):
    users = filter(lambda user: user.id == id, user_List)
    try:
     return list(users)[0]
    except:
        return {"Error":"No existe"}
#post user
@router.post("/",response_model=User,status_code=201)
async def user(user : User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="Usuario Existente")
    user_List.append(user)
    return user
#put user 
@router.put("/")
async def user(user: User):
 
 found = False

 for index, saved_user in enumerate(user_List):
    if saved_user.id == user.id:
       user_List[index]= user
       found = True

       if not found:
          return {"Error":"Usuario no Actualizado"}
       else:
          return user
#delete user       
@router.delete("/{id}")
async def userID(id: int):
    found = False
    for index, saved_user in enumerate(user_List):
     if saved_user.id == id:
       del user_List[index]
       found = True

    if not found:
     return {"Error":"No encontrado"}