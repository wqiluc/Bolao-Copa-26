from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.banco import obter_bd
import app.esquemas as esquemas
from app.service import jogos as servico_jogos

roteador = APIRouter(prefix="/jogos", tags=["jogos"])


@roteador.get("/", response_model=list[esquemas.JogoSaida])
def listar_jogos(
    id_fase: Optional[int] = None,
    id_grupo: Optional[int] = None,
    bd: Session = Depends(obter_bd),
):
    return servico_jogos.listar_jogos(bd, id_fase, id_grupo)


@roteador.get("/{id_jogo}", response_model=esquemas.JogoSaida)
def obter_jogo(id_jogo: int, bd: Session = Depends(obter_bd)):
    jogo = servico_jogos.obter_jogo(bd, id_jogo)

    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    return jogo


@roteador.put("/{id_jogo}/resultado", response_model=esquemas.JogoSaida)
def registrar_resultado(id_jogo: int, corpo: esquemas.ResultadoJogo, bd: Session = Depends(obter_bd)):
    jogo = servico_jogos.registrar_resultado(bd, id_jogo, corpo.gols_casa, corpo.gols_fora)

    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    return servico_jogos.obter_jogo(bd, id_jogo)


@roteador.put("/{id_jogo}/times", response_model=esquemas.JogoSaida)
def atualizar_times(id_jogo: int, corpo: esquemas.AtualizarTimesJogo, bd: Session = Depends(obter_bd)):
    jogo = servico_jogos.atualizar_times(bd, id_jogo, corpo.id_time_casa, corpo.id_time_fora)

    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    return jogo