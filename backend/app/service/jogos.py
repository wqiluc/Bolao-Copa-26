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


def recalcular_apostas(bd: Session, jogo: modelos.Jogo) -> None:
    if not jogo.encerrado or jogo.gols_casa is None or jogo.gols_fora is None:
        return

    valor = jogo.fase.valor
    algum_acertou = any(
        a.palpite_casa == jogo.gols_casa and a.palpite_fora == jogo.gols_fora
        for a in jogo.apostas
    )

    for aposta in jogo.apostas:
        acertou = aposta.palpite_casa == jogo.gols_casa and aposta.palpite_fora == jogo.gols_fora
        if not algum_acertou:
            aposta.pontos = 0
        elif acertou:
            aposta.pontos = valor
        else:
            aposta.pontos = -valor

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
