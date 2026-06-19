from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.banco import obter_bd
import app.esquemas as esquemas
from app.auth.auth_service import autenticar_participante

roteador = APIRouter()

@roteador.post("/auth/login", response_model=esquemas.LoginResposta)

def login(dados: esquemas.LoginEntrada, bd: Session = Depends(obter_bd)):

    participante = autenticar_participante(bd, dados.nome, dados.senha)

    if (not participante):
        raise HTTPException(status_code=401, detail="Nome ou senha incorretos.")
    else:
        return participante
