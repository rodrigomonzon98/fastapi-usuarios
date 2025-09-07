from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from passlib.hash import bcrypt

from .. import schemas, models
from ..db import get_db

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])

@router.get("", response_model=List[schemas.UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).order_by(models.Usuario.id_usuario).all()

@router.get("/{id_usuario}", response_model=schemas.UsuarioOut)
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    user = db.get(models.Usuario, id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UsuarioOut)
def crear_usuario(payload: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    hashed = bcrypt.hash(payload.password)
    user = models.Usuario(nombre=payload.nombre, correo=payload.correo, password=hashed)
    db.add(user)
    try:
        db.flush()  # asigna id
    except Exception:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario. ¿Correo duplicado?")
    return user

@router.put("/{id_usuario}", response_model=schemas.UsuarioOut)
def actualizar_usuario(id_usuario: int, payload: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    user = db.get(models.Usuario, id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    data = payload.model_dump(exclude_unset=True)
    if "password" in data and data["password"]:
        data["password"] = bcrypt.hash(data["password"])
    for k, v in data.items():
        setattr(user, k, v)
    db.add(user)
    return user

@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    user = db.get(models.Usuario, id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    return None
