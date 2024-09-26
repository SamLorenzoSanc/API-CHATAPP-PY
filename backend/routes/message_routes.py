from fastapi import APIRouter, Response, Request
from controllers.message_controller import send_logic
from models.message import MessageData
from controllers.getMessages_controller import getMessages_logic
message_router = APIRouter()

@message_router.post("/send/{id}")
async def send(request: Request, id: str, message: MessageData):
  return await send_logic(request, id, message)

@message_router.get("/{id}")
async def getMessages(request: Request, id: str):
  return await getMessages_logic(request, id)