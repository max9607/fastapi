from typing import Union
from fastapi import APIRouter, HTTPException, Depends,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

#app = FastAPI()
router = APIRouter(prefix="/login2", tags=["login2"], responses={404: {"message":"Error"}})

oauth2 = OAuth2PasswordBearer(tokenUrl= "login2")



class User(BaseModel):
    id:int
    username: str
    nombre: str
    apellidoP:str
    apellidoM:str
    edad: int
    correo: str
    disabled: bool

class UserDB(User):
    password:str
#user_List = [User(id=1, nombre="Anthony",apellidoP="Aldunate",apellidoM="Justiniano",edad=26),
#             User(id=2, nombre= "Majo",apellidoP ="Pereira",apellidoM="Aliaga",edad=26),
#             User(id=3, nombre="Kiara",apellidoP="Aldunate",apellidoM="Justiniano",edad=8)]

users_db = {
    "max9607": {
        "id": 1,
        "username": "max9607",
        "nombre": "Anthony",
        "apellidoP": "Aldunate",
        "apellidoM": "Justiniano",
        "edad": 26,
        "correo": "pelotafull@gmail.com",
        "disabled": False,
        "password": "12345",
    },
    "majo": {
        "id": 2,
        "username": "majo",
        "nombre": "Majito",
        "apellidoP": "Pereira",
        "apellidoM": "Aliaga",
        "edad": 23,
        "correo": "majo@gmail.com",
        "disabled": True,
        "password": "12345"
    }
}

def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
      

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authoriazed",headers={"auth":"bearer"})
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


@router.post("")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="nel")
    
    user = search_user(form.username)
    if form.password != user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not password")
    
    return {"token": user.username , "token_type":"bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user