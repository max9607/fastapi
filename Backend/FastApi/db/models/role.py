from pydantic import BaseModel

class Role(BaseModel):
    id:str | None
    nombre:str