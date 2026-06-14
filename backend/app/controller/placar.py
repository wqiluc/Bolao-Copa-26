from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.banco import obter_bd
import app.esquemas as esquemas
from app.service import placar as servico_placar

roteador = APIRouter(prefix="/placar", tags=["placar"])

@roteador.get("/", response_model=list[esquemas.PlacarParticipante])
def obter_placar(bd: Session = Depends(obter_bd)):
    
    bruto = servico_placar.calcular_placar(bd)

    return [
        esquemas.PlacarParticipante
        (
            participante=esquemas.ParticipanteSaida.model_validate(rota["participante"]),
            saldo_total=rota["saldo_total"],
            total_ganho=rota["total_ganho"],
            total_devido=rota["total_devido"],
            acertos_exatos=rota["acertos_exatos"],

            por_fase=[
                esquemas.PlacarFase
                (
                    fase=esquemas.FaseSaida.model_validate(fase["fase"]),
                    saldo=fase["saldo"],
                    ganho=fase["ganho"],
                    devido=fase["devido"],
                    acertos=fase["acertos"],
                )

                for fase in rota["por_fase"]
            ],
        )
        for rota in bruto
    ]