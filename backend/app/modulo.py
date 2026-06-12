from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.banco import obter_bd, engine
import app.modelos as modelos
import app.esquemas as esquemas
from app.controller import jogos as controlador_jogos
from app.controller import apostas as controlador_apostas
from app.controller import placar as controlador_placar


def criar_app() -> FastAPI:
    modelos.Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Bolão Copa do Mundo 2026", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(controlador_jogos.roteador, prefix="/api")
    app.include_router(controlador_apostas.roteador, prefix="/api")
    app.include_router(controlador_placar.roteador, prefix="/api")

    @app.get("/api/fases", response_model=list[esquemas.FaseSaida])

    def listar_fases(bd: Session = Depends(obter_bd)):
        return bd.query(modelos.Fase).order_by(modelos.Fase.ordem).all()

    @app.get("/api/times", response_model=list[esquemas.TimeSaida])

    def listar_times(bd: Session = Depends(obter_bd)):
        return bd.query(modelos.Time).order_by(modelos.Time.nome).all()

    @app.get("/api/grupos", response_model=list[esquemas.GrupoSaida])

    def listar_grupos(bd: Session = Depends(obter_bd)):
        return bd.query(modelos.Grupo).order_by(modelos.Grupo.nome).all()

    @app.get("/api/participantes", response_model=list[esquemas.ParticipanteSaida])
    
    def listar_participantes(bd: Session = Depends(obter_bd)):
        return bd.query(modelos.Participante).order_by(modelos.Participante.nome).all()

    @app.get("/saude")
    def saude():
        return {"status": "ok"}

    return app