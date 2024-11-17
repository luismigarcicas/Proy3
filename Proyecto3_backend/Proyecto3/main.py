from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine
from datetime import datetime
from typing import List
from enum import Enum

class SalaEnum(Enum):
    LAB_3 = "3.2B"
    LAB_0 = "Lab piso 0"
    
# Crear todas las tablas en la base de datos (si no existen)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#----------------------USERS--------------------------------
        # Crear un nuevo usuario
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.nombre_usuario == user.nombre_usuario).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Nombre de usuario ya registrado")
    
    db_email = db.query(models.User).filter(models.User.email == user.email).first()  # Verificamos si el email ya existe
    if db_email:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    new_user = models.User(nombre_usuario=user.nombre_usuario, contrasena=user.contrasena, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Obtener todos los usuarios
@app.get("/users/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Obtener un usuario por ID
@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    
    return {"detail": f"Usuario con email {user.email} elimi

#----------------------SALAS--------------------------------
# Crear una nueva sala
@app.post("/salas/", response_model=schemas.Sala, status_code=status.HTTP_201_CREATED)
def create_sala(sala: schemas.SalaCreate, db: Session = Depends(get_db)):
    db_sala = db.query(models.Sala).filter(models.Sala.nombre == sala.nombre).first()
    if db_sala:
        raise HTTPException(status_code=400, detail="Nombre de sala ya registrado")
    
    new_sala = models.Sala(nombre=sala.nombre, capacidad=sala.capacidad)
    db.add(new_sala)
    db.commit()
    db.refresh(new_sala)
    return new_sala

# Obtener todas las salas
@app.get("/salas/", response_model=List[schemas.Sala])
def get_salas(db: Session = Depends(get_db)):
    return db.query(models.Sala).all()

# Obtener una sala por ID
@app.get("/salas/{sala_id}", response_model=schemas.Sala)
def get_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.query(models.Sala).filter(models.Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return sala


#----------------------RESERVAS-------------------------------
# Crear una nueva reserva (sin sala_id y duración, ahora usamos SalaEnum)
@app.post("/reservas/", response_model=schemas.Reserva, status_code=status.HTTP_201_CREATED)
def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    existing_reserva = db.query(models.Reserva).filter(
        models.Reserva.fecha == reserva.fecha,
        models.Reserva.sala == reserva.sala  # Comparamos con la sala
    ).first()
    
    if existing_reserva:
        raise HTTPException(status_code=400, detail="Ya existe una reserva para esta sala en esta fecha")
    
    new_reserva = models.Reserva(
        fecha=reserva.fecha,
        descripción=reserva.descripción,
        user_id=reserva.user_id,
        sala=reserva.sala  # Usamos la sala de tipo SalaEnum
    )
    db.add(new_reserva)
    db.commit()
    db.refresh(new_reserva)
    return new_reserva

# Obtener todas las reservas
@app.get("/reservas/", response_model=List[schemas.Reserva])
def get_reservas(db: Session = Depends(get_db)):
    return db.query(models.Reserva).all()

# Obtener una reserva por ID
@app.get("/reservas/{reserva_id}", response_model=schemas.Reserva)
def get_reserva(reserva_id: str, db: Session = Depends(get_db)):
    reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

# Actualizar una reserva por ID (sin sala_id y duración, solo usamos SalaEnum)
@app.put("/reservas/{reserva_id}", response_model=schemas.Reserva)
def update_reserva(reserva_id: str, reserva_update: schemas.ReservaCreate, db: Session = Depends(get_db)):
    reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    existing_reserva = db.query(models.Reserva).filter(
        models.Reserva.fecha == reserva_update.fecha,
        models.Reserva.sala == reserva_update.sala,  # Verificamos que no exista otra reserva con la misma sala y fecha
        models.Reserva.id != reserva_id
    ).first()
    
    if existing_reserva:
        raise HTTPException(status_code=400, detail="Ya existe otra reserva para esta sala en esta fecha")
    
    reserva.fecha = reserva_update.fecha
    reserva.descripción = reserva_update.descripción
    reserva.user_id = reserva_update.user_id
    reserva.sala = reserva_update.sala  # Actualizamos la sala con el nuevo valor

    db.commit()
    db.refresh(reserva)
    return reserva

# Eliminar una reserva por ID
@app.delete("/reservas/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reserva(reserva_id: str, db: Session = Depends(get_db)):
    reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    db.delete(reserva)
    db.commit()
    return {"detail": "Reserva eliminada correctamente"}
