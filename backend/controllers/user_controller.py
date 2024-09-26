import os
from pymongo import AsyncMongoClient
from bson import ObjectId
from fastapi.responses import JSONResponse
from fastapi import Response
import datetime
MONGODB_URI = os.getenv("MONGO_DB_URI")

# Crear el cliente de MongoDB
client = AsyncMongoClient(MONGODB_URI)

# Obtener la base de datos
db = client["chat-app-crypto"]

# Función para serializar los usuarios obtenidos
def serialize_user(user):
    user["_id"] = str(user["_id"])  # Convertir ObjectId a string
    
    # Convertir cualquier campo de tipo datetime a string
    for key, value in user.items():
        if isinstance(value, datetime.datetime):
            user[key] = value.isoformat()  # Convertir fecha a string en formato ISO
    return user

# Lógica para obtener los usuarios
async def getUsersForSidebar_logic():
  try:
    # Obtener todos los usuarios de la base de datos
    users = await db.users.find().to_list(length=None)
  
    # Serializar los usuarios (convertir ObjectId a string)
    serialized_users = [serialize_user(user) for user in users]

    # Devolver la lista de usuarios en formato JSON serializable
    return JSONResponse(content={"users": serialized_users}, status_code=200)
  except Exception as e:
     # Manejar errores, devolviendo un mensaje apropiado
     return JSONResponse(content={"error": str(e)}, status_code=500)