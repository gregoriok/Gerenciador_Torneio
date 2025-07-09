# app/models.py
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base


class Time(Base):
    __tablename__ = "times"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, index=True, unique=True)
    estadio = Column(String)
    presidente = Column(String)
    image_key = Column(String, nullable=True)

    partidas_como_time1 = relationship("Partida", foreign_keys="[Partida.time1_id]", back_populates="time1")
    partidas_como_time2 = relationship("Partida", foreign_keys="[Partida.time2_id]", back_populates="time2")


class Partida(Base):
    __tablename__ = "partidas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    time1_id = Column(UUID(as_uuid=True), ForeignKey("times.id"))
    time2_id = Column(UUID(as_uuid=True), ForeignKey("times.id"))

    time1 = relationship("Time", foreign_keys=[time1_id], back_populates="partidas_como_time1")
    time2 = relationship("Time", foreign_keys=[time2_id], back_populates="partidas_como_time2")