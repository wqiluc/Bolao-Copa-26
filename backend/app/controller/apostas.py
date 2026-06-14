from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.banco import obter_bd
import app.esquemas as esquemas
from app.service import apostas as servico_apostas

roteador = APIRouter(prefix="/apostas", tags=["apostas"])

@roteador.get("/", response_model=list[esquemas.ApostaSaida])

def listar_apostas(
    id_participante: Optional[int] = None,
    id_jogo: Optional[int] = None,
    bd: Session = Depends(obter_bd),
):
    return servico_apostas.listar_apostas(bd, id_participante, id_jogo)

@roteador.post("/", response_model=esquemas.ApostaSaida, status_code=201)

def criar_aposta(corpo: esquemas.ApostaEntrada, bd: Session = Depends(obter_bd)):

    try:
        aposta = servico_apostas.criar_aposta(
            bd,
            id_participante=corpo.id_participante,
            id_jogo=corpo.id_jogo,
            palpite_casa=corpo.palpite_casa,
            palpite_fora=corpo.palpite_fora,
        )

    except IntegrityError:
        raise HTTPException(status_code=409, detail="Aposta já registrada para este jogo/participante")
    
    if (aposta is None):
        raise HTTPException(status_code=404, detail="Jogo não encontrado ou já encerrado")
    
    return aposta

@roteador.put("/{id_aposta}", response_model=esquemas.ApostaSaida)
def atualizar_aposta(id_aposta: int, corpo: esquemas.AtualizarAposta, bd: Session = Depends(obter_bd)):

    aposta = servico_apostas.atualizar_aposta(bd, id_aposta, corpo.palpite_casa, corpo.palpite_fora)

    if (aposta is None):
        raise HTTPException(status_code=404, detail="Aposta não encontrada ou jogo já encerrado")
    
    return aposta

@roteador.delete("/{id_aposta}", status_code=204)

def deletar_aposta(id_aposta: int, bd: Session = Depends(obter_bd)):
    
    ok = servico_apostas.deletar_aposta(bd, id_aposta)

    if not (ok):
        raise HTTPException(status_code=404, detail="Aposta não encontrada ou jogo já encerrado")