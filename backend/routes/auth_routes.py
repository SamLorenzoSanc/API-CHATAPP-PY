from fastapi import APIRouter, Response
from controllers.auth_controller import signup_logic, login_logic, logout_logic
from models.user import SignupData, LoginData
auth_router = APIRouter()

@auth_router.post("/signup")
async def signup(signup_data: SignupData, response: Response):
  return await signup_logic(signup_data, response)

@auth_router.post("/login")
async def login(login_data: LoginData, response: Response):
  return await login_logic(login_data, response)

@auth_router.post("/logout")
async def logout(response: Response):
  return await logout_logic(response)