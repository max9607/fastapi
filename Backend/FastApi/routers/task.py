from typing import Union
from fastapi import APIRouter, HTTPException,status
from db.models.Task import Task
from db.client import db_client
from db.schemas.Task import task_schema, tasks_schema
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends,status
from .access import get_current_user, Access


router = APIRouter(prefix="/task", tags=["task"], responses={status.HTTP_404_NOT_FOUND: {"message":"Error"}})

@router.get("/", response_model=list[Task])
async def tarea():
    return tasks_schema(db_client.task.find())

def search_task(field:str, key):
    try:
        role= db_client.task.find_one({field:key})
        return Task(**task_schema(role))
    except:
        return{"Error":"No existe"}
    

@router.post("/",response_model=Task,status_code=status.HTTP_201_CREATED)
async def creartarea(task:Task):
    if type(search_task("nombre",task.nombre)) == Task:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Tarea con el mismo nombre Existente")
    task_dict = dict(task)
    del task_dict["id"]
    task_dict["userid"] = task.userid
    id = db_client.task.insert_one(task_dict).inserted_id

    new_task = task_schema(db_client.task.find_one({"_id":id}))


    return Task(**new_task)