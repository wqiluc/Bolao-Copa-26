from sqlalchemy.orm import Session, joinedload
import app.modelos as modelos

# Mapeamento do chaveamento FIFA 2026: jogo_numero → (proximo_jogo_numero, 'casa'|'fora')
# 16avos → 8avos
CHAVE_PROXIMO_JOGO: dict[int, tuple[int, str]] = {

    73: (90, 'casa'), 74: (89, 'casa'), 75: (90, 'fora'), 76: (91, 'casa'),
    77: (89, 'fora'), 78: (91, 'fora'), 79: (92, 'casa'), 80: (92, 'fora'),
    81: (94, 'casa'), 82: (94, 'fora'), 83: (93, 'casa'), 84: (93, 'fora'),
    85: (96, 'casa'), 86: (95, 'casa'), 87: (96, 'fora'), 88: (95, 'fora'),

    # 8avos → Quartas
    89: (97, 'casa'), 90: (97, 'fora'), 91: (99, 'casa'), 92: (99, 'fora'),
    93: (98, 'casa'), 94: (98, 'fora'), 95: (100, 'casa'), 96: (100, 'fora'),

    # Quartas → Semis
    97: (101, 'casa'), 98: (101, 'fora'), 99: (102, 'casa'), 100: (102, 'fora'),

    # Semis → Final
    101: (103, 'casa'), 102: (103, 'fora'),
}


def listar_jogos(bd: Session, id_fase: int | None = None, id_grupo: int | None = None):

    q = bd.query(modelos.Jogo).options(
        joinedload(modelos.Jogo.fase),
        joinedload(modelos.Jogo.grupo),
        joinedload(modelos.Jogo.time_casa),
        joinedload(modelos.Jogo.time_fora),
    )

    if (id_fase):
        q = q.filter(modelos.Jogo.id_fase == id_fase)

    if (id_grupo):
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

    if (not jogo.encerrado or jogo.gols_casa is None or jogo.gols_fora is None):
        return

    valor = float(jogo.fase.valor)

    ganhadores = [a for a in jogo.apostas if a.palpite_casa == jogo.gols_casa and a.palpite_fora == jogo.gols_fora]

    perdedores  = [a for a in jogo.apostas if a not in ganhadores]

    if (not ganhadores):
        for aposta in (jogo.apostas):

            aposta.pontos = 0
    else:
        premio = round(valor * len(perdedores) / len(ganhadores), 2)

        for aposta in (jogo.apostas):
            if (aposta in ganhadores):
                aposta.pontos = premio
            else:
                aposta.pontos = -valor

    bd.commit()


def avancar_vencedor(bd: Session, jogo: modelos.Jogo) -> str | None:
    """Após resultado eliminatório, atribui o vencedor ao próximo jogo do chaveamento."""

    if (jogo.numero not in CHAVE_PROXIMO_JOGO):
        return None
    
    if (jogo.gols_casa is None or jogo.gols_fora is None or not jogo.encerrado):
        return None
    
    if (jogo.gols_casa == jogo.gols_fora):
        return "empate" 

    vencedor = jogo.time_casa if jogo.gols_casa > jogo.gols_fora else jogo.time_fora

    if (not vencedor):
        return None

    proximo_numero, slot = CHAVE_PROXIMO_JOGO[jogo.numero]
    
    proximo = bd.query(modelos.Jogo).filter(modelos.Jogo.numero == proximo_numero).first()

    if (not proximo):
        return None

    if (slot == 'casa'):
        proximo.id_time_casa = vencedor.id
    else:
        proximo.id_time_fora = vencedor.id

    bd.commit()

    return "ok!!❤️🏥"


def registrar_resultado(bd: Session, id_jogo: int, gols_casa: int, gols_fora: int) -> modelos.Jogo | None:

    jogo = bd.query(modelos.Jogo).filter(modelos.Jogo.id == id_jogo).first()

    if (not jogo):
        return None

    jogo.gols_casa = gols_casa
    jogo.gols_fora = gols_fora
    jogo.encerrado = True

    bd.commit()

    jogo = (
        bd.query(modelos.Jogo)
        .options(
            joinedload(modelos.Jogo.fase),
            joinedload(modelos.Jogo.apostas),
            joinedload(modelos.Jogo.time_casa),
            joinedload(modelos.Jogo.time_fora),
        )

        .filter(modelos.Jogo.id == id_jogo)
        .first()
    )

    recalcular_apostas(bd, jogo)

    if (jogo.numero in CHAVE_PROXIMO_JOGO):
        avancar_vencedor(bd, jogo)

    return jogo

def atualizar_times(bd: Session, id_jogo: int, id_time_casa: int, id_time_fora: int) -> modelos.Jogo | None:
    
    jogo = bd.query(modelos.Jogo).filter(modelos.Jogo.id == id_jogo).first()

    if not (jogo):
        return None
    
    jogo.id_time_casa = id_time_casa
    jogo.id_time_fora = id_time_fora

    bd.commit()

    return obter_jogo(bd, id_jogo)