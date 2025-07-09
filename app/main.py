from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import times, sorteio, partida


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Campeonato de Futebol",
    description="Uma API para gerenciar times, sortear partidas e transmitir eventos ao vivo."
)

app.include_router(times.router)
app.include_router(sorteio.router)
app.include_router(partida.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0", port=8000)