from typing import Union
from fastapi import APIRouter, HTTPException,status
from db.models.role import Role
from db.client import db_client
from db.schemas.role import role_schema, roles_schema
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends,status
from .access import get_current_user, Access

router = APIRouter(prefix="/roles", tags=["roles"], responses={status.HTTP_404_NOT_FOUND: {"message":"Error"}})

@router.get("/", response_model=list[Role])
async def rol(current_user:Access=Depends(get_current_user)):
    return roles_schema(db_client.roles.find())

def search_role(field:str, key):
    try:
        role= db_client.roles.find_one({field:key})
        return Role(**role_schema(role))
    except:
        return{"Error":"No existe"}
    

@router.post("/", response_model=Role,status_code=status.HTTP_201_CREATED)
async def role(role:Role,current_user:Access=Depends(get_current_user)):
    if type(search_role("nombre",role.nombre)) == Role:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="rol Existente")
    rol_dict = dict(role)
    del rol_dict["id"]
    id = db_client.roles.insert_one(rol_dict).inserted_id

    new_role = role_schema(db_client.roles.find_one({"_id":id}))

    return Role(**new_role)

@router.put("/", response_model=Role)
async def role(rol: Role,current_user:Access=Depends(get_current_user)):
    rol_dict = dict(rol)
    del rol_dict["id"]
    try:
        db_client.roles.find_one_and_replace({"_id":ObjectId(rol.id)},rol_dict)
    except:
        return{"Error":"Rol no encontrado"}
    return search_role("_id",ObjectId(rol.id))

@router.delete("/", status_code=status.HTTP_200_OK)
async def roleid(id:str,current_user:Access=Depends(get_current_user)):
    found = db_client.roles.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        return{"Error":"No encontrado"}
