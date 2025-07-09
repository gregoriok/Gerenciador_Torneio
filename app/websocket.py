from fastapi import WebSocket
from typing import Dict, List
from . import schemas
from .database import mongodb

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, partida_id: str):
        await websocket.accept()
        if partida_id not in self.active_connections:
            self.active_connections[partida_id] = []
        self.active_connections[partida_id].append(websocket)

    def disconnect(self, websocket: WebSocket, partida_id: str):
        self.active_connections[partida_id].remove(websocket)

    async def broadcast(self, message: dict, partida_id: str):
        if partida_id in self.active_connections:
            for connection in self.active_connections[partida_id]:
                await connection.send_json(message)

manager = ConnectionManager()

async def salvar_evento(evento: schemas.EventoPartida):
    collection = mongodb.get_collection("eventos_partida")
    await collection.insert_one(evento.dict())