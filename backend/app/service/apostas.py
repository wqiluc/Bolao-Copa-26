from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
import app.modelos as modelos


def carregar_aposta(bd: Session, id_aposta: int) -> modelos.Aposta | None:
    return (
        bd.query(modelos.Aposta)
        .options(
            joinedload(modelos.Aposta.participante),
            joinedload(modelos.Aposta.jogo).joinedload(modelos.Jogo.fase),
            joinedload(modelos.Aposta.jogo).joinedload(modelos.Jogo.grupo),
            joinedload(modelos.Aposta.jogo).joinedload(modelos.Jogo.time_casa),
            joinedload(modelos.Aposta.jogo).joinedload(modelos.Jogo.time_fora),
        )

        .filter(modelos.Aposta.id == id_aposta)
        .first()
    )


def listar_apostas(bd: Session, id_participante: int | None = None, id_jogo: int | None = None):

    q = bd.query(modelos.Aposta).options(
        joinedload(modelos.Aposta.participante),
        joinedload(modelos.Aposta.jogo).joinedload(modelos.Jogo.fase),
        joinedload(modelos.Aposta.jogo).joinedload(modelos.Jogo.grupo),
        joinedload(modelos.Aposta.jogo).joinedload(modelos.Jogo.time_casa),
        joinedload(modelos.Aposta.jogo).joinedload(modelos.Jogo.time_fora),
    )

    if (id_participante):
        q = q.filter(modelos.Aposta.id_participante == id_participante)

    if (id_jogo):
        q = q.filter(modelos.Aposta.id_jogo == id_jogo)

    return q.all()


def criar_aposta(
    bd: Session,
    id_participante: int,
    id_jogo: int,
    palpite_casa: int,
    palpite_fora: int,
) -> modelos.Aposta | None:
    jogo = (
        bd.query(modelos.Jogo)
        .options(joinedload(modelos.Jogo.fase))
        .filter(modelos.Jogo.id == id_jogo)
        .first()
    )

    if (not jogo) or (jogo.encerrado) or not (jogo.fase):
        return None

    aposta = modelos.Aposta(
        id_participante=id_participante,
        id_jogo=id_jogo,
        palpite_casa=palpite_casa,
        palpite_fora=palpite_fora,
        valor=jogo.fase.valor,
    )

    bd.add(aposta)

    try:
        bd.commit()
    except IntegrityError:
        bd.rollback()
        raise
    
    bd.refresh(aposta)

    return carregar_aposta(bd, aposta.id)


def atualizar_aposta(bd: Session, id_aposta: int, palpite_casa: int, palpite_fora: int) -> modelos.Aposta | None:
    aposta = (
        bd.query(modelos.Aposta)
        .options(joinedload(modelos.Aposta.jogo))
        .filter(modelos.Aposta.id == id_aposta)
        .first()
    )

    if not (aposta) or (aposta.jogo.encerrado):
        return None
    
    aposta.palpite_casa = palpite_casa
    aposta.palpite_fora = palpite_fora
    
    bd.commit()

    return carregar_aposta(bd, id_aposta)


def deletar_aposta(bd: Session, id_aposta: int) -> bool:
    aposta = (
        bd.query(modelos.Aposta)
        .options(joinedload(modelos.Aposta.jogo))
        .filter(modelos.Aposta.id == id_aposta)
        .first()
    )

    if not (aposta) or (aposta.jogo.encerrado):
        return False
    
    bd.delete(aposta)
    bd.commit()
    
    return True