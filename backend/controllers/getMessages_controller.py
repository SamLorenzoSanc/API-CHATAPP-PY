from models.message import MessageData
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import os
from pymongo import AsyncMongoClient
from bson import ObjectId
from datetime import datetime
import json

MONGODB_URI = os.getenv("MONGO_DB_URI")

# Crear el cliente de MongoDB
client = AsyncMongoClient(MONGODB_URI)

# Obtener la base de datos
db = client["chat-app-crypto"]

# Definir la función serialize_message
def serialize_message(message):
    # Implementar la lógica de serialización aquí
    pass

async def getMessages_logic(request: Request, id: str):
    user = request.state.user  # Obtener el usuario del contexto de la solicitud

    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    sender_id = user["id"]  # Obtener el ID del remitente

    # Buscar el usuario con el receiver_id en la base de datos
    receiver = await db.users.find_one({"_id": ObjectId(id)})

    if not receiver:
        raise HTTPException(status_code=404, detail="User not found")

    # Buscar una conversación existente entre el remitente y el receptor
    conversation = await db.conversations.find_one({
        "participants": {
            "$all": [ObjectId(sender_id), ObjectId(id)]
        }
    })

    if not conversation:
        # Si no existe una conversación, devolver un mensaje vacío
        return JSONResponse(content={"messages": []}, status_code=200)

    # Obtener los mensajes de la conversación
    messages = await db.messages.find({"_id": {"$in": conversation["messages"]}}).to_list(length=None)

    # Serializar los mensajes (convertir ObjectId a string)
    serialized_messages = [serialize_message(message) for message in messages]

    # Devolver la lista de mensajes en formato JSON serializable
    return JSONResponse(content={"messages": [serialized_messages]}, status_code=200)