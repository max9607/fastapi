from typing import Union
from fastapi import APIRouter, HTTPException, Depends,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "971fcdf18808f8e5970bd726ba7a5829d330061089b313bd39f8534a02bb3c77"

router = APIRouter(prefix="/loginDB2", tags=["loginDB2"], responses={404: {"message":"Error"}})

oauth2 = OAuth2PasswordBearer(tokenUrl= "loginDB")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$Zu0KYyFwxUTgH1oEAfFIqu9Y9hyV3Oi0gQuIAIMzwHSWxYx8VmFgW",
    },
    "majo": {
        "id": 2,
        "username": "majo",
        "nombre": "Majito",
        "apellidoP": "Pereira",
        "apellidoM": "Aliaga",
        "edad": 23,
        "correo": "majo@gmail.com",
        "disabled": False,
        "password": "$2a$12$5RPneytpuEHGcGh8BkQei.cThs9T3lluJkVfvIfz2.9abocrquYoa"
    }
}

def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

async def auth_user(token: str = Depends(oauth2)):
  exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authoriazed",headers={"auth":"bearer"})
  try:
    username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
    if username is None:
        raise exception
    
  except JWTError:
        raise exception
  
  return search_user(username)


async def current_user(user: UserDB = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user


@router.post("/")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="nel")
    
    user = search_user(form.username)

     
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="not password")


    access_token = {"sub":user.username, "exp": datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM) , "token_type":"bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user