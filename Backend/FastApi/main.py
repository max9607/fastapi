from typing import Union
from fastapi import FastAPI
from routers import products,users,basic_auth_users,jwt_auth_users,usersdb,roles,access,jwt_auth_usersDB

app = FastAPI()



#routers
#app.include_router(products.router)
app.include_router(users.router)
#app.include_router(basic_auth_users.router)
#app.include_router(jwt_auth_users.router)
#app.include_router(usersdb.router)
app.include_router(roles.router)
app.include_router(access.router)
#app.include_router(jwt_auth_usersDB.router)


#iniciar mongodb :  cmd mongod
#iniciar proyecto :  fastapi dev main.py

