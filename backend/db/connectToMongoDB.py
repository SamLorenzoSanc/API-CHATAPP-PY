import motor.motor_asyncio  # Asynchronous MongoDB driver
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import asyncio

# Cargar las variables de entorno del archivo .env
load_dotenv()


MONGODB_URI = os.getenv("MONGO_DB_URI")

# Crear el cliente de MongoDB
client = MongoClient(MONGODB_URI)

# Obtener la base de datos
db = client["chat-app-crypto"]




