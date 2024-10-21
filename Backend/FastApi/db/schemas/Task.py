def task_schema(task) -> dict:
    return {"id":str (task["_id"]),
            "nombre":task["nombre"],
            "fecha":task["fecha"],
            "userid":task["userid"],
            "task":task["task"],
            "completed":task["completed"]
    }

def tasks_schema(tasks) -> list:
 return [task_schema(task)for task in tasks]