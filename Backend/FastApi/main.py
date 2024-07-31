from typing import Union
from fastapi import FastAPI
from routers import products,users,basic_auth_users,jwt_auth_users,usersdb,roles,access

app = FastAPI()



#routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(usersdb.router)
app.include_router(roles.router)
app.include_router(access.router)

#iniciar mongodb :  cmd mongod
#iniciar proyecto :  fastapi dev main.py


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

