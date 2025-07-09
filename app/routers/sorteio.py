from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, FastAPI, Response
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post("/sorteio/", response_model=List[schemas.Partida], tags=["Sorteio"])
def realizar_sorteio(db: Session = Depends(get_db)):
    try:
        partidas = crud.sortear_partidas(db)
        if not partidas:
            raise HTTPException(status_code=400, detail="Não foi possível gerar partidas.")
        return partidas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/partidas/", response_model=List[schemas.Partida], tags=["Partidas"])
def listar_partidas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todas as partidas cadastradas após o sorteio.
    """
    partidas = crud.get_partidas(db=db, skip=skip, limit=limit)
    return partidas
