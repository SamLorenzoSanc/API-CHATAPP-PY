from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import os
# Clave secreta para decodificar el token JWT
SECRET_KEY = os.getenv("SECRET_KEY")
# Middleware de autenticación
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Permitir las solicitudes preflight OPTIONS sin autenticación
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # Rutas que no requieren autenticación
        if request.url.path in ["/api/auth/logout", "/api/auth/login", "/api/auth/signup", "/api/users"]:
            return await call_next(request)

        # Obtener el encabezado Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing token.")

        # Verificar el formato del encabezado Authorization
        token_parts = auth_header.split(" ")
        if len(token_parts) != 2 or token_parts[0] != "Bearer":
            raise HTTPException(status_code=401, detail="Invalid Authorization header format.")

        # Extraer el token
        token = token_parts[1]

        try:
            # Decodificar el token JWT
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token.")

            # Almacenar la información del usuario en el estado de la solicitud
            request.state.user = {"id": user_id}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token.")

        # Continuar con la solicitud
        response = await call_next(request)
        return response