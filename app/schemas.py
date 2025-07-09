# app/schemas.py
import uuid
from pydantic import BaseModel, Field
from typing import Optional

class TimeBase(BaseModel):
    nome: str
    estadio: str
    presidente: str

class TimeCreate(TimeBase):
    pass

class Time(TimeBase):
    id: uuid.UUID
    image_key: Optional[str] = None
    
    class Config:
        from_attributes = True

class PartidaBase(BaseModel):
    time1_id: uuid.UUID
    time2_id: uuid.UUID

class Partida(BaseModel):
    id: uuid.UUID
    time1: Time
    time2: Time

    class Config:
        from_attributes = True

class EventoPartida(BaseModel):
    partida_id: str
    tipo_evento: str # ex: "GOL", "CARTAO_AMARELO", "SUBSTITUICAO"
    minuto: int
    descricao: str
    jogador: Optional[str] = None