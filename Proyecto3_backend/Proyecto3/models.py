from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, DateTime, ForeignKey
from sqlalchemy.orm import relationship  # Asegúrate de importar relationship
from .database import Base
from enum import Enum

# Enum para roles de usuario
class UserRole(SQLAlchemyEnum):
    ADMIN = "admin"
    USER = "user"

# Tabla 'salas' que almacena información de las salas
class Sala(Base):
    __tablename__ = "salas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    capacidad = Column(Integer, index=True)

    # Relación uno a muchos: una sala tiene muchas reservas
    reservas = relationship("Reserva", back_populates="sitio")

# Tabla 'reservas' que almacena las reservas
class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(String, primary_key=True, index=True)
    fecha = Column(DateTime, index=True)
    duracion = Column(Integer, index=True)  # Corregí la tilde en "duración"
    descripcion = Column(String)  # Corregí la tilde en "descripción"

    # Relación muchos a uno: muchas reservas pertenecen a un usuario
    user_id = Column(String, ForeignKey("users.id"))

    # Establecemos la relación inversa con la tabla de usuarios
    dueno = relationship("User", back_populates="reservas")

    # Relación muchos a uno: muchas reservas se realizan en una sala
    sala_id = Column(Integer, ForeignKey("salas.id"))

    # Establecemos la relación inversa con la tabla de salas
    sitio = relationship("Sala", back_populates="reservas")

    
