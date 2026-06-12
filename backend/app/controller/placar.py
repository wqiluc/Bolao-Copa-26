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
            total_pontos=r["total_pontos"],
            acertos_exatos=r["acertos_exatos"],
            total_gasto=r["total_gasto"],
            por_fase=[
                esquemas.PlacarFase(
                    fase=esquemas.FaseSaida.model_validate(f["fase"]),
                    pontos=f["pontos"],
                )
                for f in r["por_fase"]
            ],
        )
        for r in bruto
    ]