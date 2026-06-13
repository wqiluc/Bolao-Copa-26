from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
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

    @app.get("/api/classificacoes")
    def classificacoes_grupos(bd: Session = Depends(obter_bd)):
        """Retorna a classificação de todos os grupos com pontos FIFA (V=3, E=1, D=0)."""
        grupos = bd.query(modelos.Grupo).order_by(modelos.Grupo.nome).all()
        resultado = []

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
                    if time and time.id not in times_map:
                        times_map[time.id] = {
                            "id": time.id, "nome": time.nome, "bandeira": time.bandeira or "",
                            "pj": 0, "v": 0, "e": 0, "d": 0, "gp": 0, "gc": 0, "pts": 0,
                        }

            for jogo in jogos_grupo:
                if not jogo.encerrado or jogo.gols_casa is None or jogo.gols_fora is None:
                    continue
                tc, tf = jogo.time_casa, jogo.time_fora
                if not tc or not tf:
                    continue
                gc, gf = jogo.gols_casa, jogo.gols_fora

                for tid, gol_pro, gol_contra in [(tc.id, gc, gf), (tf.id, gf, gc)]:
                    s = times_map[tid]
                    s["pj"] += 1; s["gp"] += gol_pro; s["gc"] += gol_contra

                if gc > gf:
                    times_map[tc.id]["v"] += 1; times_map[tc.id]["pts"] += 3
                    times_map[tf.id]["d"] += 1
                elif gc < gf:
                    times_map[tf.id]["v"] += 1; times_map[tf.id]["pts"] += 3
                    times_map[tc.id]["d"] += 1
                else:
                    times_map[tc.id]["e"] += 1; times_map[tc.id]["pts"] += 1
                    times_map[tf.id]["e"] += 1; times_map[tf.id]["pts"] += 1

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