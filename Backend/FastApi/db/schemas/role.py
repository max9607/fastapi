def role_schema(role) -> dict:
    return {"id":str (role["_id"]),
            "nombre":str (role["nombre"])
    }

def roles_schema(roles) -> list:
 return [role_schema(role)for role in roles]