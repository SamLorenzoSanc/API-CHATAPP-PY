from fastapi import APIRouter, Response, Request
from controllers.user_controller import getUsersForSidebar_logic
from fastapi.responses import JSONResponse

user_router = APIRouter()

@user_router.get("/")
async def getUsersForSidebar():
  return await getUsersForSidebar_logic()