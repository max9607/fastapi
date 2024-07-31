def user_schema(user) -> dict:
 return {  "id":str (user["_id"]),
            "nombre":str (user["nombre"]),
            "apellidoP":str (user["apellidoP"]),
            "apellidoM":str (user["apellidoM"]),
            "correo":str (user["correo"]), 
            "edad":str (user["edad"]),
            "disabled":bool(user["disabled"])
}

def users_schema(users) -> list:
 return [user_schema(user)for user in users]