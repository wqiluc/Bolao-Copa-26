"""
Seed script — idempotent. Run once on startup via Docker CMD.
Populates phases, teams, groups, matches, and participants.
"""
from datetime import datetime, timedelta
from .database import SessionLocal
from . import models


PHASES = [
    {"id": 1, "name": "Fase de Grupos",   "slug": "grupos",   "order": 1, "bet_value": 1},
    {"id": 2, "name": "16avas de Final",  "slug": "16avas",   "order": 2, "bet_value": 2},
    {"id": 3, "name": "8avas de Final",   "slug": "8avas",    "order": 3, "bet_value": 2},
    {"id": 4, "name": "Quartas de Final", "slug": "quartas",  "order": 4, "bet_value": 2},
    {"id": 5, "name": "Semifinal",        "slug": "semi",     "order": 5, "bet_value": 5},
    {"id": 6, "name": "Final",            "slug": "final",    "order": 6, "bet_value": 10},
]

PARTICIPANTS = ["Davi", "Lucas", "André", "Andrea"]

TEAMS_BY_GROUP: dict[str, list[tuple[str, str]]] = {
    "A": [
        ("Coreia do Sul",    "🇰🇷"),
        ("República Tcheca", "🇨🇿"),
        ("Marrocos",         "🇲🇦"),
        ("Venezuela",        "🇻🇪"),
    ],
    "B": [
        ("EUA",              "🇺🇸"),
        ("Inglaterra",       "🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
        ("Tunísia",          "🇹🇳"),
        ("Equador",          "🇪🇨"),
    ],
    "C": [
        ("México",           "🇲🇽"),
        ("Croácia",          "🇭🇷"),
        ("Gana",             "🇬🇭"),
        ("Jordânia",         "🇯🇴"),
    ],
    "D": [
        ("Brasil",           "🇧🇷"),
        ("Suíça",            "🇨🇭"),
        ("Arábia Saudita",   "🇸🇦"),
        ("Nova Zelândia",    "🇳🇿"),
    ],
    "E": [
        ("Argentina",        "🇦🇷"),
        ("Senegal",          "🇸🇳"),
        ("Canadá",           "🇨🇦"),
        ("Hungria",          "🇭🇺"),
    ],
    "F": [
        ("França",           "🇫🇷"),
        ("Japão",            "🇯🇵"),
        ("Uruguai",          "🇺🇾"),
        ("Iraque",           "🇮🇶"),
    ],
    "G": [
        ("Espanha",          "🇪🇸"),
        ("Austrália",        "🇦🇺"),
        ("Nigéria",          "🇳🇬"),
        ("Honduras",         "🇭🇳"),
    ],
    "H": [
        ("Portugal",         "🇵🇹"),
        ("Holanda",          "🇳🇱"),
        ("Camarões",         "🇨🇲"),
        ("Indonésia",        "🇮🇩"),
    ],
    "I": [
        ("Alemanha",         "🇩🇪"),
        ("Bélgica",          "🇧🇪"),
        ("DR Congo",         "🇨🇩"),
        ("Panamá",           "🇵🇦"),
    ],
    "J": [
        ("Itália",           "🇮🇹"),
        ("Dinamarca",        "🇩🇰"),
        ("Egito",            "🇪🇬"),
        ("Irã",              "🇮🇷"),
    ],
    "K": [
        ("Sérvia",           "🇷🇸"),
        ("Colômbia",         "🇨🇴"),
        ("Catar",            "🇶🇦"),
        ("Escócia",          "🏴󠁧󠁢󠁳󠁣󠁴󠁿"),
    ],
    "L": [
        ("Áustria",          "🇦🇹"),
        ("África do Sul",    "🇿🇦"),
        ("Costa Rica",       "🇨🇷"),
        ("Ucrânia",          "🇺🇦"),
    ],
}

GROUP_MD1: dict[str, datetime] = {
    "A": datetime(2026, 6, 11, 15, 0),
    "B": datetime(2026, 6, 12, 15, 0),
    "C": datetime(2026, 6, 13, 15, 0),
    "D": datetime(2026, 6, 14, 15, 0),
    "E": datetime(2026, 6, 15, 15, 0),
    "F": datetime(2026, 6, 16, 15, 0),
    "G": datetime(2026, 6, 17, 15, 0),
    "H": datetime(2026, 6, 18, 15, 0),
    "I": datetime(2026, 6, 19, 15, 0),
    "J": datetime(2026, 6, 20, 15, 0),
    "K": datetime(2026, 6, 21, 15, 0),
    "L": datetime(2026, 6, 22, 15, 0),
}

KNOCKOUT_GAMES: list[tuple[int, datetime, int, str]] = [
    # 16avas de Final (Round of 32) — July 5-10
    (73,  datetime(2026, 7,  5, 15, 0), 2, "1A vs 2B"),
    (74,  datetime(2026, 7,  5, 19, 0), 2, "1C vs 2D"),
    (75,  datetime(2026, 7,  6, 15, 0), 2, "1E vs 2F"),
    (76,  datetime(2026, 7,  6, 19, 0), 2, "1G vs 2H"),
    (77,  datetime(2026, 7,  7, 15, 0), 2, "1I vs 2J"),
    (78,  datetime(2026, 7,  7, 19, 0), 2, "1K vs 2L"),
    (79,  datetime(2026, 7,  8, 15, 0), 2, "2A vs 1B"),
    (80,  datetime(2026, 7,  8, 19, 0), 2, "2C vs 1D"),
    (81,  datetime(2026, 7,  9, 15, 0), 2, "2E vs 1F"),
    (82,  datetime(2026, 7,  9, 19, 0), 2, "2G vs 1H"),
    (83,  datetime(2026, 7, 10, 15, 0), 2, "2I vs 1J"),
    (84,  datetime(2026, 7, 10, 19, 0), 2, "2K vs 1L"),
    (85,  datetime(2026, 7, 11, 15, 0), 2, "3° melhor (1)"),
    (86,  datetime(2026, 7, 11, 19, 0), 2, "3° melhor (2)"),
    (87,  datetime(2026, 7, 12, 15, 0), 2, "3° melhor (3)"),
    (88,  datetime(2026, 7, 12, 19, 0), 2, "3° melhor (4)"),
    # 8avas de Final (Round of 16) — July 15-18
    (89,  datetime(2026, 7, 15, 15, 0), 3, "Jogo 73 vs Jogo 74"),
    (90,  datetime(2026, 7, 15, 19, 0), 3, "Jogo 75 vs Jogo 76"),
    (91,  datetime(2026, 7, 16, 15, 0), 3, "Jogo 77 vs Jogo 78"),
    (92,  datetime(2026, 7, 16, 19, 0), 3, "Jogo 79 vs Jogo 80"),
    (93,  datetime(2026, 7, 17, 15, 0), 3, "Jogo 81 vs Jogo 82"),
    (94,  datetime(2026, 7, 17, 19, 0), 3, "Jogo 83 vs Jogo 84"),
    (95,  datetime(2026, 7, 18, 15, 0), 3, "Jogo 85 vs Jogo 86"),
    (96,  datetime(2026, 7, 18, 19, 0), 3, "Jogo 87 vs Jogo 88"),
    # Quartas de Final — July 21-22
    (97,  datetime(2026, 7, 21, 15, 0), 4, "Jogo 89 vs Jogo 90"),
    (98,  datetime(2026, 7, 21, 19, 0), 4, "Jogo 91 vs Jogo 92"),
    (99,  datetime(2026, 7, 22, 15, 0), 4, "Jogo 93 vs Jogo 94"),
    (100, datetime(2026, 7, 22, 19, 0), 4, "Jogo 95 vs Jogo 96"),
    # Semifinal — July 25-26
    (101, datetime(2026, 7, 25, 15, 0), 5, "Jogo 97 vs Jogo 98"),
    (102, datetime(2026, 7, 26, 15, 0), 5, "Jogo 99 vs Jogo 100"),
    # Final — July 29
    (103, datetime(2026, 7, 29, 16, 0), 6, "Final"),
]


def _group_matches(
    group_name: str,
    teams: list[tuple[str, str]],
    md1_base: datetime,
    start_match_num: int,
    phase_id: int,
    group_id: int,
    team_id_map: dict[str, int],
) -> list[dict]:
    
    """
    Generate 6 group games for a group of 4 teams.
    Matchup order keeps every pair playing once:
      MD1: 0v1, 2v3   MD2: 0v2, 1v3   MD3: 0v3, 1v2 (simultaneous)
    """
    md2 = md1_base + timedelta(days=11)
    md3 = md1_base + timedelta(days=21)

    pairs = [
        (0, 1, md1_base),
        (2, 3, md1_base + timedelta(hours=4)),
        (0, 2, md2),
        (1, 3, md2 + timedelta(hours=4)),
        (0, 3, md3),
        (1, 2, md3),  
    ]

    games = []

    for i, (h, a, dt) in enumerate(pairs):
        games.append({
            "match_number": start_match_num + i,
            "match_date": dt,
            "phase_id": phase_id,
            "group_id": group_id,
            "home_team_id": team_id_map[teams[h][0]],
            "away_team_id": team_id_map[teams[a][0]],
            "description": f"Grupo {group_name}: {teams[h][0]} x {teams[a][0]}",
        })
    return games


def seed():
    db = SessionLocal()
    try:
        if db.query(models.Phase).count() > 0:
            print("Banco já populado, pulando seed.")
            return

        print("Populando o banco de dados...")

        for p in PHASES:
            db.add(models.Phase(**p))
        db.flush()

        for name in PARTICIPANTS:
            db.add(models.Participant(name=name))
        db.flush()

        group_id_map: dict[str, int] = {}
        team_id_map: dict[str, int] = {}
        group_order = list("ABCDEFGHIJKL")

        for g_name in group_order:
            grp = models.Group(name=g_name)
            db.add(grp)
            db.flush()
            group_id_map[g_name] = grp.id

            for t_name, t_flag in TEAMS_BY_GROUP[g_name]:
                team = models.Team(name=t_name, flag=t_flag)
                db.add(team)
                db.flush()
                team_id_map[t_name] = team.id

        match_num = 1
        for g_name in group_order:
            teams = TEAMS_BY_GROUP[g_name]
            games = _group_matches(
                group_name=g_name,
                teams=teams,
                md1_base=GROUP_MD1[g_name],
                start_match_num=match_num,
                phase_id=1,
                group_id=group_id_map[g_name],
                team_id_map=team_id_map,
            )
            for g in games:
                db.add(models.Match(**g))
            match_num += 6

        for mn, dt, phase_id, desc in KNOCKOUT_GAMES:
            db.add(models.Match(
                match_number=mn,
                match_date=dt,
                phase_id=phase_id,
                group_id=None,
                home_team_id=None,
                away_team_id=None,
                description=desc,
            ))

        db.commit()
        print(f"Seed concluído: {db.query(models.Match).count()} jogos criados.")

    except Exception as e:
        db.rollback()
        print(f"Erro no seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()