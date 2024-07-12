from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, database
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/atletas", response_model=schemas.Atleta)
def create_atleta(atleta: schemas.AtletaCreate, db: Session = Depends(get_db)):
    db_atleta = models.Atleta(**atleta.dict())
    try:
        db.add(db_atleta)
        db.commit()
        db.refresh(db_atleta)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=303, detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")
    return db_atleta

@app.get("/atletas", response_model=Page[schemas.Atleta])
def read_atletas(nome: Optional[str] = None, cpf: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Atleta)
    if nome:
        query = query.filter(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)
    return sqlalchemy_paginate(query)