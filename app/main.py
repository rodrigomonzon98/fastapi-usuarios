from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from .routers import users
from .db import Base, engine

app = FastAPI(title="Web Service de Usuarios", version="1.0.0")

# CORS: ajusta origins en producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas si no existen (para demo; en prod usa migraciones)
Base.metadata.create_all(bind=engine)

@app.get("/api/saludo")
def saludo():
    now = datetime.now(timezone.utc).isoformat()
    return {"mensaje": "Hola desde FastAPI en Render 👋", "fecha_hora_utc": now}

# Rutas de usuarios
app.include_router(users.router)
