from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from app.banco import obter_bd, engine
import app.modelos as modelos
import app.esquemas as esquemas
from app.controller import jogos as controlador_jogos
from app.controller import apostas as controlador_apostas
from app.controller import placar as controlador_placar
from app.auth import auth_controller as controlador_auth

def criar_app() -> FastAPI:
    modelos.Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Bolão Copa do Mundo 2026", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(controlador_auth.roteador, prefix="/api")
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

    @app.get("/api/classificacoes")

    def classificacoes_grupos(bd: Session = Depends(obter_bd)):
        """Retorna a classificação de todos os grupos com pontos FIFA (V=3, E=1, D=0)."""
        grupos = bd.query(modelos.Grupo).order_by(modelos.Grupo.nome).all()

        resultado = [ ]

        for grupo in grupos:
            jogos_grupo = (
                bd.query(modelos.Jogo)
                .options(joinedload(modelos.Jogo.time_casa), joinedload(modelos.Jogo.time_fora))
                .filter(modelos.Jogo.id_grupo == grupo.id)
                .all()
            )

            times_map: dict[int, dict] = {}

            for jogo in jogos_grupo:

                for time in (jogo.time_casa, jogo.time_fora):
                    
                    if (time and time.id not in times_map):

                        times_map[time.id] = {
                            "id": time.id, "nome": time.nome, "bandeira": time.bandeira or "", "pj": 0, "v": 0, "e": 0, "d": 0, "gp": 0, "gc": 0, "pts": 0,
                        }

            for (jogo) in jogos_grupo:

                if not (jogo.encerrado) or (jogo.gols_casa is None) or (jogo.gols_fora is None):
                    continue

                time_casa, time_fora = jogo.time_casa, jogo.time_fora

                if (not time_casa or not time_fora):
                    continue

                gols_casa, gols_fora = jogo.gols_casa, jogo.gols_fora

                for time_id, gol_pro, gol_contra in [(time_casa.id, gols_casa, gols_fora), (time_fora.id, gols_fora, gols_casa)]:

                    estat = times_map[time_id]
                    estat["pj"] += 1; estat["gp"] += gol_pro; estat["gc"] += gol_contra

                if (gols_casa > gols_fora):

                    times_map[time_casa.id]["v"] += 1; times_map[time_casa.id]["pts"] += 3
                    times_map[time_fora.id]["d"] += 1

                elif (gols_casa < gols_fora):

                    times_map[time_fora.id]["v"] += 1; times_map[time_fora.id]["pts"] += 3
                    times_map[time_casa.id]["d"] += 1

                else:
                    times_map[time_casa.id]["e"] += 1; times_map[time_casa.id]["pts"] += 1
                    times_map[time_fora.id]["e"] += 1; times_map[time_fora.id]["pts"] += 1

            classificacao = sorted(
                times_map.values(),
                key=lambda x: (-x["pts"], -(x["gp"] - x["gc"]), -x["gp"])
            )

            resultado.append({"grupo": grupo.nome, "times": classificacao})

        return resultado

    @app.get("/saude")
    def saude():
        return {"status": "running ❤️🏥"}

    return app