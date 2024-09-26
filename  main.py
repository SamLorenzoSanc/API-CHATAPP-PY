from fastapi import FastAPI
import uvicorn
from routes.auth_routes import auth_router
from routes.message_routes import message_router
from routes.user_routes import user_router
from starlette.middleware.base import BaseHTTPMiddleware
from middleware.protectRoute import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware

import os

# Cargar variables de entorno si es necesario
from dotenv import load_dotenv
load_dotenv()

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Obtener el puerto de las variables de entorno o usar el puerto 4000 por defecto
PORT = int(os.getenv("PORT", 4000))

# Definir una ruta raíz
# @app.get("/")
# def read_root():
#     return {"message": "Hello World"}

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen (solo para pruebas)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Añadir otros middlewares como el de autenticación
app.add_middleware(AuthMiddleware)

# Registrar el enrutador con el prefijo "/api/auth"
app.include_router(auth_router, prefix="/api/auth")
app.include_router(message_router, prefix="/api/messages")
app.include_router(user_router, prefix="/api/users")

# Ejecutar el servidor usando Uvicorn
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=PORT)
