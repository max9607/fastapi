from pydantic import BaseModel

class User(BaseModel):
    id:str  | None
    nombre: str
    apellidoP:str
    apellidoM:str
    correo:str
    edad: int
    disabled:bool = False
