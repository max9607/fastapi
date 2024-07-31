from pydantic import BaseModel

class Access(BaseModel):
    id:str | None
    correo_usuario: str
    nombre_rol: str
    password: str
    disabled: bool = False