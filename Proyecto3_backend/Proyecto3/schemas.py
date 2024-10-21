from pydantic import BaseModel
from typing import List, Optional  # Asegúrate de importar Optional
from enum import Enum

# Enum para roles de usuario (reutilizando el mismo Enum que en models.py)
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

# Esquema base para usuarios
class UserBase(BaseModel):
    nombre_usuario: str
    contrasena: str
    role: Optional[UserRole] = UserRole.USER

# Esquema para mostrar un usuario
class User(UserBase):
    id: str
    reservas: List["Reserva"] = []  # Lista de reservas asociadas con el usuario

    class Config:
        orm_mode = True  # Habilita el modo ORM para trabajar con SQLAlchemy

# Esquema base para salas
class SalaBase(BaseModel):
    nombre: str
    capacidad: int

# Esquema para mostrar una sala
class Sala(SalaBase):
    id: int
    reservas: List["Reserva"] = []  # Lista de reservas asociadas con la sala

    class Config:
        orm_mode = True  # Habilita el modo ORM para trabajar con SQLAlchemy

# Asegúrate de definir la clase Reserva si no está definida en otro lugar
class Reserva(BaseModel):  # Asegúrate de que esta clase esté definida
    id: str
    user_id: str
    sala_id: int

    class Config:
        orm_mode = True
