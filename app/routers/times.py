from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, FastAPI, Response
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
import os
import boto3
import base64
import json

aws_session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

router = APIRouter()
@router.post("/times/", response_model=schemas.Time, tags=["Times"])
def criar_time(time: schemas.TimeCreate, db: Session = Depends(get_db)):
    db_time = crud.get_time_by_nome(db, nome=time.nome)
    if db_time:
        raise HTTPException(status_code=400, detail="Time com este nome já cadastrado")
    return crud.create_time(db=db, time=time)


@router.get("/times/", response_model=List[schemas.Time], tags=["Times"])
def listar_times(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    times = crud.get_times(db, skip=skip, limit=limit)
    return times


@router.post("/{time_id}/imagem", tags=["Times"])
async def upload_imagem_time(
        time_id: str,
        db: Session = Depends(get_db),
        file: UploadFile = File(...)
):
    db_time = crud.get_time_by_id(db=db, time_id=time_id)
    if not db_time:
        raise HTTPException(status_code=404, detail="Time não encontrado")

    file_content = await file.read()
    payload = {
        "file_content": base64.b64encode(file_content).decode('utf-8'),
        "content_type": file.content_type
    }

    lambda_client = aws_session.client('lambda')
    response = lambda_client.invoke(
        FunctionName=os.getenv("LAMBDA_FUNCTION_NAME"),
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )

    response_payload = json.load(response['Payload'])
    if response_payload.get('statusCode') != 200:
        raise HTTPException(status_code=500, detail="Erro ao fazer upload da imagem.")

    s3_key = response_payload['body']['s3_key']
    crud.update_time_image_key(db=db, time_id=time_id, image_key=s3_key)

    return {"message": "Imagem enviada com sucesso!", "s3_key": s3_key}


@router.get("/{time_id}/imagem-url",tags=["Times"])
def get_imagem_url_time(time_id: str, db: Session = Depends(get_db)):
    db_time = crud.get_time_by_id(db=db, time_id=time_id)
    if not db_time or not db_time.image_key:
        raise HTTPException(status_code=404, detail="Imagem não encontrada para este time")

    s3_client = aws_session.client('s3')
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': os.getenv("S3_BUCKET"), 'Key': db_time.image_key},
            ExpiresIn=3600
        )
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Não foi possível gerar a URL da imagem.")
