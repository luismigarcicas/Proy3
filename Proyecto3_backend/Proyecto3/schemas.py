from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from sqlalchemy import Column, String, Enum as SQLAlchemyEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class SalaEnum(SQLAlchemyEnum ):
    LAB_3 = "3.2B"
    LAB_0 = "Lab piso 0"

# Esquema base para usuarios
class UserBase(BaseModel):
    nombre_usuario: str
    contrasena: str
    email:strg

# Esquema para mostrar un usuario
class User(UserBase):
    id: str
    reservas: List["Reserva"] = []  # Lista de reservas asociadas con el usuario

    class Config:
        orm_mode = True  # Habilita el modo ORM para trabajar con SQLAlchemy


# Asegúrate de definir la clase Reserva si no está definida en otro lugar
class Reserva(BaseModel):
    id: str
    user_id: str
    sala: SalaEnum = SalaEnum.LAB_0  

    class Config:
        orm_mode = True
