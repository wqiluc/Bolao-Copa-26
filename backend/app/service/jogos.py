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

# Seeding fase de grupos → 16avas: (nome_grupo, posicao) → (numero_jogo, 'casa'|'fora')
# Bracket oficial FIFA Copa 26 (jogos 73-88)
SEEDING_1_2: dict[tuple[str, int], tuple[int, str]] = {
    ('A', 1): (79, 'casa'), ('A', 2): (73, 'casa'),
    ('B', 1): (85, 'casa'), ('B', 2): (73, 'fora'),
    ('C', 1): (76, 'casa'), ('C', 2): (75, 'fora'),
    ('D', 1): (81, 'casa'), ('D', 2): (88, 'casa'),
    ('E', 1): (74, 'casa'), ('E', 2): (78, 'casa'),
    ('F', 1): (75, 'casa'), ('F', 2): (76, 'fora'),
    ('G', 1): (82, 'casa'), ('G', 2): (88, 'fora'),
    ('H', 1): (84, 'casa'), ('H', 2): (86, 'fora'),
    ('I', 1): (77, 'casa'), ('I', 2): (78, 'fora'),
    ('J', 1): (86, 'casa'), ('J', 2): (84, 'fora'),
    ('K', 1): (87, 'casa'), ('K', 2): (83, 'casa'),
    ('L', 1): (80, 'casa'), ('L', 2): (83, 'fora'),
}

# Grupos aceitos em cada slot de 3° colocado (sempre como 'fora')
TERCEIROS_SLOTS: dict[int, set[str]] = {
    74: {'A', 'B', 'C', 'D', 'F'},
    77: {'C', 'D', 'F', 'G', 'H'},
    79: {'C', 'E', 'F', 'H', 'I'},
    80: {'E', 'H', 'I', 'J', 'K'},
    81: {'B', 'E', 'F', 'I', 'J'},
    82: {'A', 'E', 'H', 'I', 'J'},
    85: {'E', 'F', 'G', 'I', 'J'},
    87: {'D', 'E', 'I', 'J', 'L'},
}


def _classificar_grupo(bd: Session, id_grupo: int) -> list[dict]:
    """Retorna times do grupo ordenados por colocação (pontos → saldo → gols marcados)."""
    jogos = bd.query(modelos.Jogo).filter_by(id_grupo=id_grupo, encerrado=True).all()

    times_ids: set[int] = set()
    for j in jogos:
        if j.id_time_casa: times_ids.add(j.id_time_casa)
        if j.id_time_fora: times_ids.add(j.id_time_fora)

    stats: dict[int, dict] = {tid: {'pontos': 0, 'gf': 0, 'gc': 0} for tid in times_ids}

    for j in jogos:
        if j.gols_casa is None or j.gols_fora is None:
            continue
        c, f, gc, gf = j.id_time_casa, j.id_time_fora, j.gols_casa, j.gols_fora
        stats[c]['gf'] += gc; stats[c]['gc'] += gf
        stats[f]['gf'] += gf; stats[f]['gc'] += gc
        if gc > gf:   stats[c]['pontos'] += 3
        elif gc < gf: stats[f]['pontos'] += 3
        else:         stats[c]['pontos'] += 1; stats[f]['pontos'] += 1

    ordenados = sorted(
        stats.items(),
        key=lambda x: (-x[1]['pontos'], -(x[1]['gf'] - x[1]['gc']), -x[1]['gf'])
    )
    return [
        {'time': bd.query(modelos.Time).filter_by(id=tid).first(),
         'pontos': s['pontos'], 'saldo': s['gf'] - s['gc'], 'gf': s['gf']}
        for tid, s in ordenados
    ]


def semear_grupo_no_mata_mata(bd: Session, id_grupo: int) -> bool:
    """Popula slots de 1° e 2° do grupo nas 16avas. Só age quando o grupo estiver completo."""
    grupo = bd.query(modelos.Grupo).filter_by(id=id_grupo).first()
    if not grupo:
        return False

    total = bd.query(modelos.Jogo).filter_by(id_grupo=id_grupo, id_fase=1).count()
    enc   = bd.query(modelos.Jogo).filter_by(id_grupo=id_grupo, id_fase=1, encerrado=True).count()
    if total == 0 or total != enc:
        return False

    for posicao, classif in enumerate(_classificar_grupo(bd, id_grupo)[:2], start=1):
        chave = (grupo.nome, posicao)
        if chave not in SEEDING_1_2:
            continue
        num_destino, slot = SEEDING_1_2[chave]
        jogo_destino = bd.query(modelos.Jogo).filter_by(numero=num_destino).first()
        if not jogo_destino:
            continue
        if slot == 'casa':
            jogo_destino.id_time_casa = classif['time'].id
        else:
            jogo_destino.id_time_fora = classif['time'].id

    bd.commit()
    return True


def _bipartite_match(grupos: list[str], slots: dict[int, set[str]]) -> dict[int, str]:
    """Matching bipartido (Hopcroft-Karp simplificado): slot → grupo."""
    match: dict[int, str] = {}

    def augment(slot: int, visitados: set[str]) -> bool:
        for grupo in grupos:
            if grupo not in slots[slot] or grupo in visitados:
                continue
            visitados.add(grupo)
            slot_atual = next((s for s, g in match.items() if g == grupo), None)
            if slot_atual is None or augment(slot_atual, visitados):
                match[slot] = grupo
                return True
        return False

    for slot in slots:
        augment(slot, set())
    return match


def semear_terceiros(bd: Session) -> dict:
    """
    Calcula os 8 melhores 3° colocados e os distribui nos slots das 16avas via matching bipartido.
    Só executa após todos os 12 grupos estarem concluídos.
    """
    grupos = bd.query(modelos.Grupo).order_by(modelos.Grupo.nome).all()

    for grupo in grupos:
        total = bd.query(modelos.Jogo).filter_by(id_grupo=grupo.id, id_fase=1).count()
        enc   = bd.query(modelos.Jogo).filter_by(id_grupo=grupo.id, id_fase=1, encerrado=True).count()
        if total != enc:
            return {'erro': f'Grupo {grupo.nome} incompleto ({enc}/{total} jogos encerrados)'}

    terceiros = []
    for grupo in grupos:
        classif = _classificar_grupo(bd, grupo.id)
        if len(classif) >= 3:
            t = classif[2]
            terceiros.append({'grupo': grupo.nome, 'time': t['time'],
                              'pontos': t['pontos'], 'saldo': t['saldo'], 'gf': t['gf']})

    terceiros.sort(key=lambda x: (-x['pontos'], -x['saldo'], -x['gf']))
    qualificados = terceiros[:8]
    grupos_qualificados = [t['grupo'] for t in qualificados]

    atribuicao = _bipartite_match(grupos_qualificados, TERCEIROS_SLOTS)
    mapa = {t['grupo']: t for t in qualificados}

    for slot_num, grupo_nome in atribuicao.items():
        jogo = bd.query(modelos.Jogo).filter_by(numero=slot_num).first()
        if jogo:
            jogo.id_time_fora = mapa[grupo_nome]['time'].id
    bd.commit()

    return {
        'qualificados': [{'grupo': t['grupo'], 'time': t['time'].nome,
                          'pontos': t['pontos'], 'saldo': t['saldo']} for t in qualificados],
        'atribuicao': {slot: mapa[g]['time'].nome for slot, g in atribuicao.items()},
    }


def semear_todos_grupos(bd: Session) -> dict:
    """Semeia todos os grupos já concluídos (retroativo). Retorna quantos foram semeados."""
    grupos = bd.query(modelos.Grupo).all()
    semeados = [g.nome for g in grupos if semear_grupo_no_mata_mata(bd, g.id)]
    return {'semeados': semeados, 'total': len(semeados)}


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
        pool_cents = round(valor * len(perdedores) * 100)
        n = len(ganhadores)
        base_cents = pool_cents // n
        extra = pool_cents % n

        idx = 0
        
        for aposta in (jogo.apostas):

            if (aposta in ganhadores):
                cents = base_cents + (1 if idx < extra else 0)
                aposta.pontos = round(cents / 100, 2)
                idx += 1
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

    if jogo.id_fase == 1 and jogo.id_grupo:
        semear_grupo_no_mata_mata(bd, jogo.id_grupo)
    elif jogo.numero in CHAVE_PROXIMO_JOGO:
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