from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    correo: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=4, max_length=100)

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    correo: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=4, max_length=100)

class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_usuario: int
    nombre: str
    correo: EmailStr
    fecha_reg: datetime
