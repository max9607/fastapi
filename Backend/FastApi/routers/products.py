from fastapi import FastAPI, HTTPException
from fastapi import APIRouter


router = APIRouter(prefix="/products", tags=["products"], responses={404: {"message":"Error"}})

product_list = ["P1","p2","P3","P4"]

@router.get("/")
async def products():
    return product_list

@router.get("/{id}")
async def products(id: int ):
    return product_list[id]


