from typing import Union
from fastapi import FastAPI
from routers import products,users,basic_auth_users,jwt_auth_users,usersdb,roles,access,jwt_auth_usersDB

app = FastAPI()



#routers
#app.include_router(products.router)

#app.include_router(basic_auth_users.router)
#app.include_router(jwt_auth_users.router)
#app.include_router(usersdb.router)
app.include_router(usersdb.router)
app.include_router(roles.router)
app.include_router(access.router)
#app.include_router(jwt_auth_usersDB.router)


#iniciar mongodb :  cmd mongod
#iniciar proyecto :  fastapi dev main.py

#iniciar mongodb :  cmd mongod
#iniciar proyecto :  fastapi dev main.py
#iniciar mongodb :  cmd mongod
#iniciar proyecto :  fastapi dev main.py - uvicorn main:app --reload
#instalar antes para correr el proyecto 
#pip install fastapi - pip install uvicorn
#verificar si esta instalado 
#pip show uvicorn

#agregar el path en variable de entorno de windows y ejecutar el entorno virtual de python 
#C:\Users\Anthony\source\repos\FastApiWithSql\Python\myenv\Scripts\Activate

#en caso de que no se pueda añadir a las variables de entorno
#C:\Users\Anthony\source\repos\FastApiWithSql\Python\myenv\Scripts\uvicorn.exe main:app --reload

#crear entorno virtual
#python -m venv C:\Users\Anthony\source\repos\FastApiSql\FastApiWithSql\myenv
#C:\Users\Anthony\source\repos\FastApi\python

#intstalar
#pip install "fastapi[standard]"
#pip install bson
#pip install python-jose[cryptography]
#pip install passlib
