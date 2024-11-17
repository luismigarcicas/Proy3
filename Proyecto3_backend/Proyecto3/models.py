from sqlalchemy import Column, String, Enum as SQLAlchemyEnum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.types import Enum

# Enum para las salas usando SQLAlchemyEnum directamente
class SalaEnum(SQLAlchemyEnum):
    LAB_3 = "3.2B"
    LAB_0 = "Lab piso 0"

# Tabla 'users' que almacena información de los usuarios
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    nombre_usuario = Column(String, unique=True, index=True, nullable=False)
    contrasena = Column(String, nullable=False)  # Contraseña del usuario
    email = Column(String, unique=True, index=True, nullable=True)  # Email del usuario (opcional)

    # Relación uno a muchos: un usuario tiene muchas reservas
    reservas = relationship("Reserva", back_populates="dueno")

    def __repr__(self):
        return f"<User(id={self.id}, nombre_usuario={self.nombre_usuario}, email={self.email})>"

# Tabla 'reservas' que almacena las reservas
class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(String, primary_key=True, index=True)
    fecha = Column(DateTime, index=True, default=func.now())  # Fecha de la reserva
    descripcion = Column(String, nullable=True)  # Descripción opcional

    # Relación muchos a uno: muchas reservas pertenecen a un usuario
    user_id = Column(String, ForeignKey("users.id"))

    # Establecemos la relación inversa con la tabla de usuarios
    dueno = relationship("User", back_populates="reservas")

    # Relación uno a uno: cada reserva debe estar asociada a una sala
    sala = Column(SQLAlchemyEnum(SalaEnum), nullable=False)  # Sala de la reserva

    # Timestamps: fechas de creación y actualización
    created_at = Column(DateTime, default=func.now())  # Fecha de creación
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Fecha de última actualización

    def __repr__(self):
        return f"<Reserva(id={self.id}, user_id={self.user_id}, sala={self.sala}, fecha={self.fecha})>"
