# app/crud.py
from sqlalchemy.orm import Session, joinedload
import random
from . import models, schemas

def get_time_by_id(db: Session, time_id: str):
    return db.query(models.Time).filter(models.Time.id == time_id).first()
def get_time_by_nome(db: Session, nome: str):
    return db.query(models.Time).filter(models.Time.nome == nome).first()
def get_times(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Time).offset(skip).limit(limit).all()

def create_time(db: Session, time: schemas.TimeCreate):
    db_time = models.Time(nome=time.nome, estadio=time.estadio, presidente=time.presidente)
    db.add(db_time)
    db.commit()
    db.refresh(db_time)
    return db_time

def update_time_image_key(db: Session, time_id: str, image_key: str) -> models.Time:
    db_time = get_time_by_id(db=db, time_id=time_id)
    if db_time:
        db_time.image_key = image_key
        db.commit()
        db.refresh(db_time)
    return db_time

def sortear_partidas(db: Session):

    partidas_existentes = db.query(models.Partida).first()
    if partidas_existentes:
        raise ValueError(
            "Um sorteio já foi realizado. Para sortear novamente, as partidas existentes precisam ser removidas.")

    times = get_times(db)
    if len(times) < 2:
        raise ValueError("Não há times suficientes para o sorteio.")

    random.shuffle(times)

    partidas_criadas = []

    if len(times) % 2 != 0:
        times.pop()

    for i in range(0, len(times), 2):
        time1 = times[i]
        time2 = times[i + 1]

        db_partida = models.Partida(time1_id=time1.id, time2_id=time2.id)
        db.add(db_partida)
        partidas_criadas.append(db_partida)

    db.commit()

    for p in partidas_criadas:
        db.refresh(p)

    return partidas_criadas

def get_partidas(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Partida)
        .options(
            joinedload(models.Partida.time1),
            joinedload(models.Partida.time2)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )