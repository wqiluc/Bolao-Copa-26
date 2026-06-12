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
        esquemas.PlacarParticipante(
            participante=esquemas.ParticipanteSaida.model_validate(r["participante"]),
            saldo_total=r["saldo_total"],
            acertos_exatos=r["acertos_exatos"],
            por_fase=[
                esquemas.PlacarFase(
                    fase=esquemas.FaseSaida.model_validate(f["fase"]),
                    saldo=f["saldo"],
                )
                for f in r["por_fase"]
            ],
        )
        for r in bruto
    ]