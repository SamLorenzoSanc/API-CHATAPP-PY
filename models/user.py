from pydantic import BaseModel

class SignupData(BaseModel):
  full_name: str
  username: str
  password: str
  confirm_password: str
  email: str
  gender: str

class LoginData(BaseModel):
  username: str
  password: str
