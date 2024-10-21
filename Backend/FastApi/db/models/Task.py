from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    id : str | None
    nombre: str
    fecha : datetime
    userid: str
    task  : str
    completed: bool = False

