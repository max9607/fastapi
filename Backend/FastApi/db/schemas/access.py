def access_schema(access) -> dict:
    return {
        "id": str(access["_id"]),
        "correo_usuario": access["correo_usuario"],
        "nombre_rol": access["nombre_rol"],
        "password": access["password"],
        "disabled": access["disabled"]
    }

def acces_schema(acces)-> list:
    return[access_schema(access)for access in acces]