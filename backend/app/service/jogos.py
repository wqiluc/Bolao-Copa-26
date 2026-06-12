from sqlalchemy.orm import Session, joinedload
import app.modelos as modelos


def listar_jogos(bd: Session, id_fase: int | None = None, id_grupo: int | None = None):
    q = bd.query(modelos.Jogo).options(
        joinedload(modelos.Jogo.fase),
        joinedload(modelos.Jogo.grupo),
        joinedload(modelos.Jogo.time_casa),
        joinedload(modelos.Jogo.time_fora),
    )
    if id_fase:
        q = q.filter(modelos.Jogo.id_fase == id_fase)
    if id_grupo:
        q = q.filter(modelos.Jogo.id_grupo == id_grupo)
    return q.order_by(modelos.Jogo.data, modelos.Jogo.numero).all()


def obter_jogo(bd: Session, id_jogo: int) -> modelos.Jogo | None:
    return (
        bd.query(modelos.Jogo)
        .options(
            joinedload(modelos.Jogo.fase),
            joinedload(modelos.Jogo.grupo),
            joinedload(modelos.Jogo.time_casa),
            joinedload(modelos.Jogo.time_fora),
        )
        .filter(modelos.Jogo.id == id_jogo)
        .first()
    )


def calcular_pontos(palpite_casa: int, palpite_fora: int, gols_casa: int, gols_fora: int) -> int:
    if palpite_casa == gols_casa and palpite_fora == gols_fora:
        return 3
    return 0


def recalcular_apostas(bd: Session, jogo: modelos.Jogo) -> None:
    if not jogo.encerrado or jogo.gols_casa is None or jogo.gols_fora is None:
        return
    for aposta in jogo.apostas:
        aposta.pontos = calcular_pontos(
            aposta.palpite_casa, aposta.palpite_fora,
            jogo.gols_casa, jogo.gols_fora,
        )
    bd.commit()


def registrar_resultado(bd: Session, id_jogo: int, gols_casa: int, gols_fora: int) -> modelos.Jogo | None:
    jogo = bd.query(modelos.Jogo).filter(modelos.Jogo.id == id_jogo).first()
    if not jogo:
        return None
    jogo.gols_casa = gols_casa
    jogo.gols_fora = gols_fora
    jogo.encerrado = True
    bd.commit()
    bd.refresh(jogo)
    recalcular_apostas(bd, jogo)
    return jogo


def atualizar_times(bd: Session, id_jogo: int, id_time_casa: int, id_time_fora: int) -> modelos.Jogo | None:
    jogo = bd.query(modelos.Jogo).filter(modelos.Jogo.id == id_jogo).first()
    if not jogo:
        return None
    jogo.id_time_casa = id_time_casa
    jogo.id_time_fora = id_time_fora
    bd.commit()
    return obter_jogo(bd, id_jogo)
