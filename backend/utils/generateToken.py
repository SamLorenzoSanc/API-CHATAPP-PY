import jwt
import datetime
from datetime import datetime, timedelta
import os
# Clave secreta para firmar el token

SECRET_KEY = os.getenv("SECRET_KEY")

def create_jwt_token(user_id: str) -> str:
    # Definir la carga útil (payload) del token
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Expira en 1 hora
    }
    # Generar el token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt_token(token: str):
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "El token ha expirado"
    except jwt.InvalidTokenError:
        return "Token inválido"