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

# Función para serializar objetos datetime a formato ISO 8601
def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

async def send_logic(request: Request, id: str, message: MessageData):
  
  user = request.state.user  # Obtener el usuario del contexto de la solicitud
  sender_id = user["id"]  # Obtener el ID del remitente
    
  # Buscar el usuario con el receiver_id en la base de datos
  receiver = await db.users.find_one({"_id": ObjectId(id)})
  
  if not receiver:
      raise HTTPException(status_code=404, detail="User not found")
  
  # Crear el mensaje que será almacenado en la colección de mensajes
  new_message = {
      "sender_id": ObjectId(sender_id),
      "receiver_id": ObjectId(id),
      "message": message.message,
      "createdAt": datetime.utcnow(),
      "updatedAt": datetime.utcnow()
  }
  # Insertar el mensaje en la colección de mensajes y obtener su ID
  result = await db.messages.insert_one(new_message)
  message_id = result.inserted_id
  # Buscar una conversación existente entre el remitente y el receptor
  conversation = await db.conversations.find_one({
      "participants": {
          "$all": [ObjectId(sender_id), ObjectId(id)]
      }
  })
  if conversation:
      # Si la conversación existe, agregar el mensaje a la conversación
      await db.conversations.update_one(
          {"_id": conversation["_id"]}, 
          {
              "$push": {"messages": message_id},  # Agregar el ID del mensaje
              "$set": {"updatedAt": datetime.utcnow()}  # Actualizar la fecha
          }
      )
  else:
      # Si no existe la conversación, crear una nueva
      new_conversation = {
          "participants": [ObjectId(sender_id), ObjectId(id)],  # Lista de participantes
          "messages": [message_id],  # Lista de IDs de mensajes
          "createdAt": datetime.utcnow(),
          "updatedAt": datetime.utcnow(),
      }
      await db.conversations.insert_one(new_conversation)
  # Devolver la conversación actualizada como respuesta
  updated_conversation = await db.conversations.find_one({"participants": {"$all": [ObjectId(sender_id), ObjectId(id)]}})
  
  # Convertir ObjectId a string antes de devolver la conversación
  updated_conversation["_id"] = str(updated_conversation["_id"])
  updated_conversation["participants"] = [str(p) for p in updated_conversation["participants"]]
  updated_conversation["messages"] = [str(m) for m in updated_conversation["messages"]]

  return JSONResponse(content=json.loads(json.dumps(updated_conversation, default=serialize_datetime)), status_code=201)
