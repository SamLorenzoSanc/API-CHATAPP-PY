from db.connectToMongoDB import db
from fastapi import HTTPException, Response
from models.user import SignupData, LoginData
from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from passlib.context import CryptContext
from utils.generateToken import create_jwt_token
import os
import bcrypt
from fastapi.responses import JSONResponse

# Cargar las variables de entorno del archivo .env
load_dotenv()


MONGODB_URI = os.getenv("MONGO_DB_URI")

# Crear el cliente de MongoDB
client = AsyncMongoClient(MONGODB_URI)

# Obtener la base de datos
db = client["chat-app-crypto"]

# Definir contexto para hashear las contraseñas (usando passlib)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def signup_logic(user: SignupData, response: Response):
   # Verificar si el nombre de usuario ya existe
    
  existing_user = await db.users.find_one({"username": user.username})
  if existing_user:
    raise HTTPException(status_code=400, detail="Username already exists")
  if user.password != user.confirm_password:
    raise HTTPException(status_code=400, detail="Passwords do not match")
  
  # Guardar el usuario en la base de datos
  user_dict = user.dict()
  
  # Aquí puedes agregar lógica para no almacenar `confirm_password`
  del user_dict["confirm_password"]  # Eliminar confirm_password del dict
  
  boy_profile_picture = "https://avatar.iran.liara.run/public/boy?username=" + user_dict["username"]
  girl_profile_picture = "https://avatar.iran.liara.run/public/girl?username=" + user_dict["username"]
  
  user_dict["profile_picture"] = boy_profile_picture if user_dict["gender"] == "male" else girl_profile_picture

  # Hashear contraseña
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(user_dict["password"].encode('utf-8'), salt)
  user_dict["password"] = hashed_password.decode('utf-8')

  # Convertir ObjectId a string antes de devolver
  result = await db.users.insert_one(user_dict)
  user_dict["_id"] = str(result.inserted_id)

  token = create_jwt_token(user_dict["_id"])
  # Almacenar el token en una cookie
  response.set_cookie(key="jwt_token", value=token, httponly=True, secure=True)
  return {"message": "User created successfully", "user": user_dict}

async def login_logic(login_data: LoginData, response: Response):
    try:
        user = await db.users.find_one({"username": login_data.username})

        if not user:
            return JSONResponse(status_code=400, content={"error": "Invalid username or password"})

        # Verificar si la contraseña proporcionada coincide con la almacenada
        if not verify_password(login_data.password, user["password"]):
            return JSONResponse(status_code=400, content={"error": "Invalid username or password"})

        # Generar un token JWT si las credenciales son correctas
        token = create_jwt_token(str(user["_id"]))

        # Guardar el token en una cookie HTTPOnly
        response.set_cookie(key="jwt_token", value=token, httponly=True, secure=True)

        return JSONResponse(status_code=200, content={
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
                "profile_picture": user.get("profilePic", None)  # Usa get() para evitar KeyError si no existe "profilePic"
            })
    except Exception as e:
        # Manejo general de errores
        return JSONResponse(status_code=500, content={"error": str(e)})

async def logout_logic(response: Response):
  # Eliminar la cookie que contiene el token
  response.delete_cookie(key="jwt_token")
  return {"message": "Logout succesful"}