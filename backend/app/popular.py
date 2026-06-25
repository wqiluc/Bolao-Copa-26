from datetime import datetime as dt
from sqlalchemy import text
from app.banco import SessaoLocal, engine
import app.modelos as modelos
from app.auth.auth_service import criar_hash_senha

def _migrar_schema():
    with engine.connect() as conn:
        conn.execute(text(
            "ALTER TABLE participantes ADD COLUMN IF NOT EXISTS senha_hash VARCHAR(100)"
        ))

        # Corrige eliminatórias: horários em BRT (UTC-3)
        conn.execute(text("""
            UPDATE jogos SET data = CASE numero
                WHEN 73  THEN '2026-06-28 16:00:00'::TIMESTAMP
                WHEN 74  THEN '2026-06-29 17:00:00'::TIMESTAMP
                WHEN 75  THEN '2026-06-29 22:00:00'::TIMESTAMP
                WHEN 76  THEN '2026-06-29 14:00:00'::TIMESTAMP
                WHEN 77  THEN '2026-06-30 18:00:00'::TIMESTAMP
                WHEN 78  THEN '2026-06-30 14:00:00'::TIMESTAMP
                WHEN 79  THEN '2026-06-30 22:00:00'::TIMESTAMP
                WHEN 80  THEN '2026-07-01 13:00:00'::TIMESTAMP
                WHEN 81  THEN '2026-07-01 21:00:00'::TIMESTAMP
                WHEN 82  THEN '2026-07-03 18:00:00'::TIMESTAMP
                WHEN 83  THEN '2026-07-03 22:00:00'::TIMESTAMP
                WHEN 84  THEN '2026-07-01 16:00:00'::TIMESTAMP
                WHEN 85  THEN '2026-07-03 00:00:00'::TIMESTAMP
                WHEN 86  THEN '2026-07-02 19:00:00'::TIMESTAMP
                WHEN 87  THEN '2026-07-02 22:00:00'::TIMESTAMP
                WHEN 88  THEN '2026-07-03 15:00:00'::TIMESTAMP
                WHEN 89  THEN '2026-07-04 14:00:00'::TIMESTAMP
                WHEN 90  THEN '2026-07-04 18:00:00'::TIMESTAMP
                WHEN 91  THEN '2026-07-05 14:00:00'::TIMESTAMP
                WHEN 92  THEN '2026-07-05 18:00:00'::TIMESTAMP
                WHEN 93  THEN '2026-07-06 14:00:00'::TIMESTAMP
                WHEN 94  THEN '2026-07-06 18:00:00'::TIMESTAMP
                WHEN 95  THEN '2026-07-07 14:00:00'::TIMESTAMP
                WHEN 96  THEN '2026-07-07 18:00:00'::TIMESTAMP
                WHEN 97  THEN '2026-07-09 16:00:00'::TIMESTAMP
                WHEN 98  THEN '2026-07-09 20:00:00'::TIMESTAMP
                WHEN 99  THEN '2026-07-10 16:00:00'::TIMESTAMP
                WHEN 100 THEN '2026-07-10 20:00:00'::TIMESTAMP
                WHEN 101 THEN '2026-07-14 16:00:00'::TIMESTAMP
                WHEN 102 THEN '2026-07-15 16:00:00'::TIMESTAMP
                WHEN 103 THEN '2026-07-19 16:00:00'::TIMESTAMP
            END
            WHERE numero BETWEEN 73 AND 103
        """))

        # Corrige fase de grupos: subtrai 3h (UTC → BRT) se ainda estiver em UTC
        # Detecta pelo jogo 13 (Brasil vs Marrocos): UTC=19h, BRT=16h
        conn.execute(text("""
            UPDATE jogos SET data = data - INTERVAL '3 hours'
            WHERE numero BETWEEN 1 AND 72
              AND EXISTS (
                SELECT 1 FROM jogos g2
                WHERE g2.numero = 13
                  AND g2.data >= '2026-06-13 17:00:00'::TIMESTAMP
              )
        """))

        conn.commit()

SENHA_PADRAO = "03070203"

FASES = [
    {"id": 1, "nome": "Fase de Grupos",   "slug": "grupos",   "ordem": 1, "valor": 1},
    {"id": 2, "nome": "16avas de Final",  "slug": "16avas",   "ordem": 2, "valor": 2},
    {"id": 3, "nome": "8avas de Final",   "slug": "8avas",    "ordem": 3, "valor": 2},
    {"id": 4, "nome": "Quartas de Final", "slug": "quartas",  "ordem": 4, "valor": 2},
    {"id": 5, "nome": "Semifinal",        "slug": "semi",     "ordem": 5, "valor": 5},
    {"id": 6, "nome": "Final",            "slug": "final",    "ordem": 6, "valor": 10},
]

PARTICIPANTES = ["Davi", "Lucas", "André", "Andrea"]

TIMES_POR_GRUPO: dict[str, list[tuple[str, str]]] = {
    "A": [("México", "🇲🇽"), ("África do Sul", "🇿🇦"), ("Coreia do Sul", "🇰🇷"), ("Tchéquia", "🇨🇿")],
    "B": [("Canadá", "🇨🇦"), ("Bósnia", "🇧🇦"), ("Catar", "🇶🇦"), ("Suíça", "🇨🇭")],
    "C": [("Brasil", "🇧🇷"), ("Marrocos", "🇲🇦"), ("Haiti", "🇭🇹"), ("Escócia", "🏴󠁧󠁢󠁳󠁣󠁴󠁿")],
    "D": [("EUA", "🇺🇸"), ("Paraguai", "🇵🇾"), ("Austrália", "🇦🇺"), ("Turquia", "🇹🇷")],
    "E": [("Alemanha", "🇩🇪"), ("Curaçao", "🇨🇼"), ("Costa do Marfim", "🇨🇮"), ("Equador", "🇪🇨")],
    "F": [("Holanda", "🇳🇱"), ("Japão", "🇯🇵"), ("Suécia", "🇸🇪"), ("Tunísia", "🇹🇳")],
    "G": [("Bélgica", "🇧🇪"), ("Egito", "🇪🇬"), ("Irã", "🇮🇷"), ("Nova Zelândia", "🇳🇿")],
    "H": [("Espanha", "🇪🇸"), ("Cabo Verde", "🇨🇻"), ("Arábia Saudita", "🇸🇦"), ("Uruguai", "🇺🇾")],
    "I": [("França", "🇫🇷"), ("Senegal", "🇸🇳"), ("Iraque", "🇮🇶"), ("Noruega", "🇳🇴")],
    "J": [("Argentina", "🇦🇷"), ("Argélia", "🇩🇿"), ("Áustria", "🇦🇹"), ("Jordânia", "🇯🇴")],
    "K": [("Portugal", "🇵🇹"), ("RD Congo", "🇨🇩"), ("Uzbequistão", "🇺🇿"), ("Colômbia", "🇨🇴")],
    "L": [("Inglaterra", "🏴󠁧󠁢󠁥󠁮󠁧󠁿"), ("Croácia", "🇭🇷"), ("Gana", "🇬🇭"), ("Panamá", "🇵🇦")],
}


JOGOS_GRUPOS: list[tuple[int, dt, str, str, str, str | None]] = [

    # GRUPO A
    (1,  dt(2026, 6, 11, 13,  0), "A", "México",          "África do Sul",   None),
    (2,  dt(2026, 6, 11, 20,  0), "A", "Coreia do Sul",   "Tchéquia",        None),
    (3,  dt(2026, 6, 18, 10,  0), "A", "Tchéquia",        "África do Sul",   "Atlanta"),
    (4,  dt(2026, 6, 18, 19,  0), "A", "México",          "Coreia do Sul",   "Guadalajara"),
    (5,  dt(2026, 6, 24, 19,  0), "A", "Tchéquia",        "México",          "Cidade do México"),
    (6,  dt(2026, 6, 24, 19,  0), "A", "África do Sul",   "Coreia do Sul",   "Monterrey"),

    # GRUPO B
    (7,  dt(2026, 6, 12, 13,  0), "B", "Canadá",          "Bósnia",          "Toronto"),
    (8,  dt(2026, 6, 13, 13,  0), "B", "Catar",           "Suíça",           "San Francisco"),
    (9,  dt(2026, 6, 18, 13,  0), "B", "Suíça",           "Bósnia",          "Los Angeles"),
    (10, dt(2026, 6, 18, 16,  0), "B", "Canadá",          "Catar",           "Vancouver"),
    (11, dt(2026, 6, 24, 13,  0), "B", "Suíça",           "Canadá",          "Vancouver"),
    (12, dt(2026, 6, 24, 13,  0), "B", "Bósnia",          "Catar",           "Seattle"),

    # GRUPO C
    (13, dt(2026, 6, 13, 16,  0), "C", "Brasil",          "Marrocos",        "Nova York/NJ"),
    (14, dt(2026, 6, 13, 19,  0), "C", "Haiti",           "Escócia",         "Boston"),
    (15, dt(2026, 6, 19, 16,  0), "C", "Escócia",         "Marrocos",        "Boston"),
    (16, dt(2026, 6, 19, 19,  0), "C", "Brasil",          "Haiti",           "Filadélfia"),
    (17, dt(2026, 6, 24, 16,  0), "C", "Escócia",         "Brasil",          "Miami"),
    (18, dt(2026, 6, 24, 16,  0), "C", "Marrocos",        "Haiti",           "Atlanta"),

    # GRUPO D
    (19, dt(2026, 6, 12, 19,  0), "D", "EUA",             "Paraguai",        "Los Angeles"),
    (20, dt(2026, 6, 13, 22,  0), "D", "Austrália",       "Turquia",         "Vancouver"),
    (21, dt(2026, 6, 19, 21,  0), "D", "Turquia",         "Paraguai",        "San Francisco"),
    (22, dt(2026, 6, 19, 13,  0), "D", "EUA",             "Austrália",       "Seattle"),
    (23, dt(2026, 6, 25, 20,  0), "D", "Turquia",         "EUA",             "Los Angeles"),
    (24, dt(2026, 6, 25, 20,  0), "D", "Paraguai",        "Austrália",       "San Francisco"),

    # GRUPO E
    (25, dt(2026, 6, 14, 11,  0), "E", "Alemanha",        "Curaçao",         "Houston"),
    (26, dt(2026, 6, 14, 17,  0), "E", "Costa do Marfim", "Equador",         "Filadélfia"),
    (27, dt(2026, 6, 20, 14,  0), "E", "Alemanha",        "Costa do Marfim", "Toronto"),
    (28, dt(2026, 6, 20, 18,  0), "E", "Equador",         "Curaçao",         "Kansas City"),
    (29, dt(2026, 6, 25, 14,  0), "E", "Equador",         "Alemanha",        "Nova York/NJ"),
    (30, dt(2026, 6, 25, 14,  0), "E", "Curaçao",         "Costa do Marfim", "Filadélfia"),

    # GRUPO F
    (31, dt(2026, 6, 14, 14,  0), "F", "Holanda",         "Japão",           "Dallas"),
    (32, dt(2026, 6, 14, 20,  0), "F", "Suécia",          "Tunísia",         "Monterrey"),
    (33, dt(2026, 6, 20, 11,  0), "F", "Holanda",         "Suécia",          "Houston"),
    (34, dt(2026, 6, 20, 22,  0), "F", "Tunísia",         "Japão",           "Monterrey"),
    (35, dt(2026, 6, 25, 17,  0), "F", "Japão",           "Suécia",          "Dallas"),
    (36, dt(2026, 6, 25, 17,  0), "F", "Tunísia",         "Holanda",         "Kansas City"),

    # GRUPO G
    (37, dt(2026, 6, 15, 13,  0), "G", "Bélgica",         "Egito",           "Seattle"),
    (38, dt(2026, 6, 15, 19,  0), "G", "Irã",             "Nova Zelândia",   "Los Angeles"),
    (39, dt(2026, 6, 21, 13,  0), "G", "Bélgica",         "Irã",             "Los Angeles"),
    (40, dt(2026, 6, 21, 19,  0), "G", "Nova Zelândia",   "Egito",           "Vancouver"),
    (41, dt(2026, 6, 26, 21,  0), "G", "Egito",           "Irã",             "Seattle"),
    (42, dt(2026, 6, 26, 21,  0), "G", "Nova Zelândia",   "Bélgica",         "Vancouver"),

    # GRUPO H
    (43, dt(2026, 6, 15, 10,  0), "H", "Espanha",         "Cabo Verde",      "Atlanta"),
    (44, dt(2026, 6, 15, 16,  0), "H", "Arábia Saudita",  "Uruguai",         "Miami"),
    (45, dt(2026, 6, 21, 10,  0), "H", "Espanha",         "Arábia Saudita",  "Atlanta"),
    (46, dt(2026, 6, 21, 16,  0), "H", "Uruguai",         "Cabo Verde",      "Miami"),
    (47, dt(2026, 6, 26, 18,  0), "H", "Cabo Verde",      "Arábia Saudita",  "Houston"),
    (48, dt(2026, 6, 26, 18,  0), "H", "Uruguai",         "Espanha",         "Guadalajara"),

    # GRUPO I
    (49, dt(2026, 6, 16, 13,  0), "I", "França",          "Senegal",         "Nova York/NJ"),
    (50, dt(2026, 6, 16, 16,  0), "I", "Iraque",          "Noruega",         "Boston"),
    (51, dt(2026, 6, 22, 15,  0), "I", "França",          "Iraque",          "Filadélfia"),
    (52, dt(2026, 6, 22, 18,  0), "I", "Noruega",         "Senegal",         "Nova York/NJ"),
    (53, dt(2026, 6, 26, 13,  0), "I", "Noruega",         "França",          "Boston"),
    (54, dt(2026, 6, 26, 13,  0), "I", "Senegal",         "Iraque",          "Toronto"),

    # GRUPO J
    (55, dt(2026, 6, 16, 19,  0), "J", "Argentina",       "Argélia",         "Kansas City"),
    (56, dt(2026, 6, 16, 22,  0), "J", "Áustria",         "Jordânia",        "San Francisco"),
    (57, dt(2026, 6, 22, 11,  0), "J", "Argentina",       "Áustria",         "Dallas"),
    (58, dt(2026, 6, 22, 21,  0), "J", "Jordânia",        "Argélia",         "San Francisco"),
    (59, dt(2026, 6, 27, 20,  0), "J", "Argélia",         "Áustria",         "Kansas City"),
    (60, dt(2026, 6, 27, 20,  0), "J", "Jordânia",        "Argentina",       "Dallas"),

    # GRUPO K
    (61, dt(2026, 6, 17, 11,  0), "K", "Portugal",        "RD Congo",        "Houston"),
    (62, dt(2026, 6, 17, 20,  0), "K", "Uzbequistão",     "Colômbia",        "Cidade do México"),
    (63, dt(2026, 6, 23, 11,  0), "K", "Portugal",        "Uzbequistão",     "Houston"),
    (64, dt(2026, 6, 23, 20,  0), "K", "Colômbia",        "RD Congo",        "Guadalajara"),
    (65, dt(2026, 6, 27, 17, 30), "K", "Colômbia",        "Portugal",        "Miami"),
    (66, dt(2026, 6, 27, 17, 30), "K", "RD Congo",        "Uzbequistão",     "Atlanta"),

    # GRUPO L
    (67, dt(2026, 6, 17, 14,  0), "L", "Inglaterra",      "Croácia",         "Dallas"),
    (68, dt(2026, 6, 17, 17,  0), "L", "Gana",            "Panamá",          "Toronto"),
    (69, dt(2026, 6, 23, 14,  0), "L", "Inglaterra",      "Gana",            "Boston"),
    (70, dt(2026, 6, 23, 17,  0), "L", "Panamá",          "Croácia",         "Toronto"),
    (71, dt(2026, 6, 27, 15,  0), "L", "Panamá",          "Inglaterra",      "Nova York/NJ"),
    (72, dt(2026, 6, 27, 15,  0), "L", "Croácia",         "Gana",            "Filadélfia"),
]

# Jogos das fases eliminatórias — times definidos conforme times se classificam
# Todos os horários em BRT (UTC-3)

JOGOS_ELIMINATORIAS: list[tuple[int, dt, int, str]] = [
    # 16avos de Final — 28 jun a 03 jul 2026
    # Jun 28
    (73,  dt(2026, 6, 28, 16,  0), 2, "16avos: Jogo 1"),   # 12h ET — África do Sul vs Canadá
    # Jun 29
    (76,  dt(2026, 6, 29, 14,  0), 2, "16avos: Jogo 4"),   # 10h ET — Brasil vs 2° Grupo F
    (74,  dt(2026, 6, 29, 17,  0), 2, "16avos: Jogo 2"),   # 13h ET — Alemanha vs 3°
    (75,  dt(2026, 6, 29, 22,  0), 2, "16avos: Jogo 3"),   # 18h ET — 1° Grupo F vs Marrocos
    # Jun 30
    (78,  dt(2026, 6, 30, 14,  0), 2, "16avos: Jogo 6"),   # 10h ET — 2° Grupo E vs 2° Grupo I
    (77,  dt(2026, 6, 30, 18,  0), 2, "16avos: Jogo 5"),   # 14h ET — 1° Grupo I vs 3°
    (79,  dt(2026, 6, 30, 22,  0), 2, "16avos: Jogo 7"),   # 18h ET — México vs 3°
    # Jul 1
    (80,  dt(2026, 7,  1, 13,  0), 2, "16avos: Jogo 8"),   #  9h ET — 1° Grupo L vs 3°
    (84,  dt(2026, 7,  1, 16,  0), 2, "16avos: Jogo 12"),  # 12h ET — Espanha vs 2° Grupo J
    (81,  dt(2026, 7,  1, 21,  0), 2, "16avos: Jogo 9"),   # 17h ET — EUA vs 3°
    # Jul 2
    (86,  dt(2026, 7,  2, 19,  0), 2, "16avos: Jogo 14"),  # 15h ET — Argentina vs Uruguai
    (87,  dt(2026, 7,  2, 22,  0), 2, "16avos: Jogo 15"),  # 18h ET — 1° Grupo K vs 3°
    (85,  dt(2026, 7,  3,  0,  0), 2, "16avos: Jogo 13"),  # 20h ET — Suíça vs 3°
    # Jul 3
    (88,  dt(2026, 7,  3, 15,  0), 2, "16avos: Jogo 16"),  # 11h ET — 2° Grupo D vs 2° Grupo G
    (82,  dt(2026, 7,  3, 18,  0), 2, "16avos: Jogo 10"),  # 14h ET — 1° Grupo G vs 3°
    (83,  dt(2026, 7,  3, 22,  0), 2, "16avos: Jogo 11"),  # 18h ET — 2° Grupo K vs 2° Grupo L

    # 8avos de Final — 04 a 07 jul 2026
    (89,  dt(2026, 7,  4, 14,  0), 3, "8avos: Jogo 1"),
    (90,  dt(2026, 7,  4, 18,  0), 3, "8avos: Jogo 2"),
    (91,  dt(2026, 7,  5, 14,  0), 3, "8avos: Jogo 3"),
    (92,  dt(2026, 7,  5, 18,  0), 3, "8avos: Jogo 4"),
    (93,  dt(2026, 7,  6, 14,  0), 3, "8avos: Jogo 5"),
    (94,  dt(2026, 7,  6, 18,  0), 3, "8avos: Jogo 6"),
    (95,  dt(2026, 7,  7, 14,  0), 3, "8avos: Jogo 7"),
    (96,  dt(2026, 7,  7, 18,  0), 3, "8avos: Jogo 8"),

    # Quartas de Final — 09 a 10 jul 2026
    (97,  dt(2026, 7,  9, 16,  0), 4, "Quartas: Jogo 1"),
    (98,  dt(2026, 7,  9, 20,  0), 4, "Quartas: Jogo 2"),
    (99,  dt(2026, 7, 10, 16,  0), 4, "Quartas: Jogo 3"),
    (100, dt(2026, 7, 10, 20,  0), 4, "Quartas: Jogo 4"),

    # Semifinal — 14 e 15 jul 2026
    (101, dt(2026, 7, 14, 16,  0), 5, "Semifinal: Jogo 1"),
    (102, dt(2026, 7, 15, 16,  0), 5, "Semifinal: Jogo 2"),

    # Final — 19 jul 2026 — MetLife Stadium, Nova York/NJ
    (103, dt(2026, 7, 19, 16,  0), 6, "Final"),
]


def popular(reset: bool = False):
    if (reset):
        modelos.Base.metadata.drop_all(bind=engine)
        print("Tabelas removidas.")

    modelos.Base.metadata.create_all(bind=engine)
    _migrar_schema()

    bd = SessaoLocal()

    try:
        if not (reset) and (bd.query(modelos.Fase).count() > 0):
            sem_senha = bd.query(modelos.Participante).filter(modelos.Participante.senha_hash == None).all()

            if (sem_senha):
                print(f"Adicionando senha padrão a {len(sem_senha)} participantes sem hash...")

                hash_padrao = criar_hash_senha(SENHA_PADRAO)

                for p in sem_senha:
                    p.senha_hash = hash_padrao
                bd.commit()

            else:
                print("Banco já populado, pulando.")
            return

        else:
            print("Populando o banco de dados...")

        for fase in FASES:
            bd.add(modelos.Fase(**fase))
        bd.flush()

        hash_padrao = criar_hash_senha(SENHA_PADRAO)

        for nome in PARTICIPANTES:
            bd.add(modelos.Participante(nome=nome, senha_hash=hash_padrao))
        bd.flush()

        mapa_id_grupo: dict[str, int] = { }
        mapa_id_time: dict[str, int] = { }

        for nome_grupo, times in TIMES_POR_GRUPO.items():

            grupo = modelos.Grupo(nome=nome_grupo)
            bd.add(grupo)
            bd.flush()
            mapa_id_grupo[nome_grupo] = grupo.id

            for nome_time, bandeira in times:

                time = modelos.Time(nome=nome_time, bandeira=bandeira)
                bd.add(time)
                bd.flush()
                mapa_id_time[nome_time] = time.id

        for num, dt, grp, casa, fora, local in (JOGOS_GRUPOS):

            bd.add(modelos.Jogo(
                numero=num,
                data=dt,
                id_fase=1,
                id_grupo=mapa_id_grupo[grp],
                id_time_casa=mapa_id_time[casa],
                id_time_fora=mapa_id_time[fora],
                descricao=f"Grupo {grp}: {casa} × {fora}",
                local=local,
            ))

        for num, dt, id_fase, desc in (JOGOS_ELIMINATORIAS):

            bd.add(modelos.Jogo(
                numero=num,
                data=dt,
                id_fase=id_fase,
                id_grupo=None,
                id_time_casa=None,
                id_time_fora=None,
                descricao=desc,
                local=None,
            ))

        bd.commit()

        print(f"Banco Populado: {bd.query(modelos.Jogo).count()} jogos criados.")

    except Exception as e:
        bd.rollback()
        print(f"Erro ao popular: {e}")
        raise
    finally:
        bd.close()

if (__name__ == "__main__"):
    import sys
    popular(reset="--reset" in sys.argv)
