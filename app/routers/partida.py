from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from .. import schemas
from app.websocket import manager, salvar_evento

router = APIRouter()

@router.websocket("/ws/partida/{partida_id}")
async def websocket_endpoint(websocket: WebSocket, partida_id: str):
    await manager.connect(websocket, partida_id)
    try:
        while True:
            data = await websocket.receive_json()
            try:
                evento = schemas.EventoPartida(partida_id=partida_id, **data)
            except Exception as e:
                await websocket.send_json({"error": "Formato de evento inválido.", "details": str(e)})
                continue

            await salvar_evento(evento)

            await manager.broadcast(evento.dict(), partida_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, partida_id)
        await manager.broadcast({"message": "Um usuário desconectou."}, partida_id)

@router.get("/ws/partida/{partida_id}",
    tags=["WebSocket (Documentação)"],
    summary="Documentação para Conexão WebSocket da Partida",
    description="""
    Este endpoint é para estabelecer uma conexão WebSocket e receber eventos de uma partida em tempo real.
    
    **Para usar, não faça uma requisição GET. Em vez disso, conecte-se a esta mesma URL usando um cliente WebSocket (ex: `ws://127.0.0.1:8000/ws/partida/{partida_id}`).**
    
    ### Mensagens (Cliente -> Servidor)
    Para registrar um evento na partida, envie uma mensagem em formato JSON com a seguinte estrutura:
    ```json
    {
      "tipo_evento": "GOL",
      "minuto": 42,
      "descricao": "Gol de bicicleta!",
      "jogador": "Craque da Silva"
    }
```
""",
)
async def documentacao_websocket(partida_id: int):
    """
    Este endpoint é apenas para documentação. Para usar WebSocket, conecte-se via ws://
    """
    raise HTTPException(status_code=400, detail="Use WebSocket para conectar-se a este endpoint.")
