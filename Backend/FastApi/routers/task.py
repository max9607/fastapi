from typing import Union
from fastapi import APIRouter, HTTPException,status
from db.models.Task import Task
from db.client import db_client
from db.schemas.Task import task_schema, tasks_schema
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends,status
from .access import get_current_user, Access


router = APIRouter(prefix="/task", tags=["task"], responses={status.HTTP_404_NOT_FOUND: {"message":"Error"}})


#metodo que nos devuelve todas las tareas
@router.get("/", response_model=list[Task])
async def tarea():
    return tasks_schema(db_client.task.find())


@router.get("/{id}", response_model=Task,status_code=status.HTTP_200_OK)
async def tareaid(id:str):
    return search_task("_id", ObjectId(id))


def search_task(field:str, key):
    try:
        role= db_client.task.find_one({field:key})
        return Task(**task_schema(role))
    except:
        return{"Error":"No existe"}
    
#metodo que nos permite crear una tarea
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

#metodo que nos permite editar una tarea
@router.put("/", response_model=Task, status_code=status.HTTP_200_OK)
async def Editarea(task:Task):
    task_dic = dict(task)
    del task_dic["id"]
    try:
        db_client.task.find_one_and_replace({"_id": ObjectId(task.id)},task_dic)
    except:
        return{"Error":"tarea no encontrada"}
    return search_task("_id",ObjectId(task.id))

#metodo que nos permite eliminar una tarea
@router.delete("/",status_code=status.HTTP_200_OK)
async def deletetarea(id:str):
    found = db_client.task.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        return{"Error":"No encontrado"}


#metodo que nos permite editar el estado de una tarea
@router.patch("/{id}", response_model=Task, status_code=status.HTTP_200_OK)
async def editar_estado_tarea(id: str):
    found = db_client.task.find_one({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    db_client.task.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"completed": True}})
    updated_task = db_client.task.find_one({"_id": ObjectId(id)})
    task_response = {
        "id": str(updated_task["_id"]),  
        "nombre": updated_task["nombre"],
        "fecha": updated_task["fecha"],
        "userid": updated_task["userid"],
        "task": updated_task["task"],
        "completed": updated_task["completed"]
    }
    return Task(**task_response)

