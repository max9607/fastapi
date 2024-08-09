from typing import Union
from fastapi import APIRouter, HTTPException,status
from db.client import db_client
from bson import ObjectId
from db.models.user import User
from db.models.role import Role
from db.models.access import Access
from db.schemas.user import user_schema, users_schema
from db.schemas.role import role_schema, roles_schema
from db.schemas.access import access_schema, acces_schema
from fastapi import APIRouter, HTTPException, Depends,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30
SECRET = "971fcdf18808f8e5970bd726ba7a5829d330061089b313bd39f8534a02bb3c77"

router = APIRouter(prefix="/access", tags=["access"], responses={status.HTTP_404_NOT_FOUND: {"message":"Error"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="access/login")


crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def search_user(correo:str):
    user = db_client.users.find_one({"correo":correo})
    return user

def search_role(rol:str):
    role = db_client.roles.find_one({"nombre":rol})
    return role

def search_acces(correo:str):
    acces = db_client.acceces.find_one({"correo":correo })
    return acces

def get_password_hash(password:str)-> str:
    return crypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt.verify(plain_password, hashed_password)

async def auth_user(token: str = Depends(oauth2)):
  exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authoriazed",headers={"auth":"bearer"})
  try:
    username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
    if username is None:
        raise exception
    
  except JWTError:
        raise exception
  
  return search_user(username)

async def get_current_user(acces: Access = Depends(auth_user)):
    if acces['disabled']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return acces


@router.post("/", response_model=Access, status_code=status.HTTP_201_CREATED)
async def register(accces:Access):
    user = search_user(accces.correo_usuario)
    if not user:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="usuario no encontrado")
    
    role = search_role(accces.nombre_rol)
    if not role:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="rol no encontrado")
    
    hashed_password = get_password_hash(accces.password)
    accces_dict = accces.dict()
    accces_dict["password"]= hashed_password

    if "id" in accces_dict:
        del accces_dict["id"]

    insert= db_client.acceces.insert_one(accces_dict)
    new_access = db_client.acceces.find_one({"_id": insert.inserted_id})
    return Access(**access_schema(new_access))



@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    access = db_client.acceces.find_one({"correo_usuario": form.username})

    if not access:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no encontrado")


    stored_password = access.get("password", "")


    if not stored_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña no encontrada")


    try:
        if not crypt.verify(form.password, stored_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Contraseña incorrecta")
    except Exception as e:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error en la verificación de contraseña")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = jwt.encode(
                {"sub": form.username, "exp": datetime.utcnow() + access_token_expires},SECRET,algorithm=ALGORITHM)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=list[Access])
async def me(current_user:Access = Depends(get_current_user)):
 return acces_schema(db_client.acceces.find())  
