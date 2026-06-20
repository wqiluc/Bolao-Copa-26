<h1 align="center">🏅 Tracker de Colocados — Copa do Mundo 2026<br>
<img src="https://img.shields.io/badge/Copa_2026-Classificados-111827?style=flat-square&logo=fifa&logoColor=yellow"/></h1>

<p align="center">
  Referência completa do sistema de classificação: grupos, seeding e chaveamento eliminatório.<br>
  O backend popula automaticamente os slots das 16avas conforme os grupos são concluídos via <code>semear_grupo_no_mata_mata()</code> e <code>semear_terceiros()</code>.
</p>

## 📋 Critérios de Classificação

### Fase de Grupos

Cada grupo tem **4 times** disputando entre si em turno único (**6 jogos/grupo**, 72 no total).

| Critério de desempate | Regra |
|---|---|
| 1° | Pontos (V=3, E=1, D=0) |
| 2° | Saldo de gols (gols marcados − sofridos) |
| 3° | Gols marcados |

- **1° e 2° de cada grupo** → classificados diretos (24 vagas)
- **8 melhores 3° colocados** entre os 12 grupos → classificados por ranking (8 vagas)
- Total: **32 classificados** para as 16avas de final

## 🏆 Grupos — Times e Destino no Seeding

> Fonte: `SEEDING_1_2` em [`backend/app/service/jogos.py`](../backend/app/service/jogos.py)

| Grupo | Times | 1° → 16avos | 2° → 16avos |
|---|---|---|---|
| **A** | 🇲🇽 México · 🇿🇦 África do Sul · 🇰🇷 Coreia do Sul · 🇨🇿 Tchéquia | Jogo 79 (casa) | Jogo 73 (casa) |
| **B** | 🇨🇦 Canadá · 🇧🇦 Bósnia · 🇶🇦 Catar · 🇨🇭 Suíça | Jogo 85 (casa) | Jogo 73 (fora) |
| **C** | 🇧🇷 Brasil · 🇲🇦 Marrocos · 🇭🇹 Haiti · 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escócia | Jogo 76 (casa) | Jogo 75 (fora) |
| **D** | 🇺🇸 EUA · 🇵🇾 Paraguai · 🇦🇺 Austrália · 🇹🇷 Turquia | Jogo 81 (casa) | Jogo 88 (casa) |
| **E** | 🇩🇪 Alemanha · 🇨🇼 Curaçao · 🇨🇮 Costa do Marfim · 🇪🇨 Equador | Jogo 74 (casa) | Jogo 78 (casa) |
| **F** | 🇳🇱 Holanda · 🇯🇵 Japão · 🇸🇪 Suécia · 🇹🇳 Tunísia | Jogo 75 (casa) | Jogo 76 (fora) |
| **G** | 🇧🇪 Bélgica · 🇪🇬 Egito · 🇮🇷 Irã · 🇳🇿 Nova Zelândia | Jogo 82 (casa) | Jogo 88 (fora) |
| **H** | 🇪🇸 Espanha · 🇨🇻 Cabo Verde · 🇸🇦 Arábia Saudita · 🇺🇾 Uruguai | Jogo 84 (casa) | Jogo 86 (fora) |
| **I** | 🇫🇷 França · 🇸🇳 Senegal · 🇮🇶 Iraque · 🇳🇴 Noruega | Jogo 77 (casa) | Jogo 78 (fora) |
| **J** | 🇦🇷 Argentina · 🇩🇿 Argélia · 🇦🇹 Áustria · 🇯🇴 Jordânia | Jogo 86 (casa) | Jogo 84 (fora) |
| **K** | 🇵🇹 Portugal · 🇨🇩 RD Congo · 🇺🇿 Uzbequistão · 🇨🇴 Colômbia | Jogo 87 (casa) | Jogo 83 (casa) |
| **L** | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra · 🇭🇷 Croácia · 🇬🇭 Gana · 🇵🇦 Panamá | Jogo 80 (casa) | Jogo 83 (fora) |

## 🥉 3° Colocados — Ranking e Distribuição

Os **12 terceiros colocados** são ordenados por pontos → saldo → gols. Os **8 melhores** avançam e são distribuídos nos 8 slots disponíveis das 16avas via **matching bipartido** (`_bipartite_match` em `service/jogos.py`).

> Endpoint: `POST /api/jogos/semear_terceiros` — só executa após todos os 12 grupos encerrados.

### Slots disponíveis para 3° colocados

> Fonte: `TERCEIROS_SLOTS` em [`backend/app/service/jogos.py`](../backend/app/service/jogos.py)

| Jogo 16avos | Slot | Grupos elegíveis |
|---|---|---|
| Jogo 74 | fora | A, B, C, D, F |
| Jogo 77 | fora | C, D, F, G, H |
| Jogo 79 | fora | C, E, F, H, I |
| Jogo 80 | fora | E, H, I, J, K |
| Jogo 81 | fora | B, E, F, I, J |
| Jogo 82 | fora | A, E, H, I, J |
| Jogo 85 | fora | E, F, G, I, J |
| Jogo 87 | fora | D, E, I, J, L |

> O algoritmo garante que cada 3° classificado cai em um slot compatível com seu grupo de origem. Se nenhuma atribuição válida existe para algum grupo, o slot não é preenchido (empate não resolvido → `PUT /api/jogos/{id}/times`).

## ⚔️ Chaveamento das 16avas de Final

> Jogos de 05 a 12 de julho de 2026 · Fonte: `CHAVE_PROXIMO_JOGO` em [`backend/app/service/jogos.py`](../backend/app/service/jogos.py)

```
Jogo 73  │ A2        vs  B2        │ → vencedor → Jogo 90 (casa)
Jogo 74  │ E1        vs  3°(A/B/C/D/F) │ → vencedor → Jogo 89 (casa)
Jogo 75  │ F1        vs  C2        │ → vencedor → Jogo 90 (fora)
Jogo 76  │ C1        vs  F2        │ → vencedor → Jogo 91 (casa)
Jogo 77  │ I1        vs  3°(C/D/F/G/H) │ → vencedor → Jogo 89 (fora)
Jogo 78  │ E2        vs  I2        │ → vencedor → Jogo 91 (fora)
Jogo 79  │ A1        vs  3°(C/E/F/H/I) │ → vencedor → Jogo 92 (casa)
Jogo 80  │ L1        vs  3°(E/H/I/J/K) │ → vencedor → Jogo 92 (fora)
Jogo 81  │ D1        vs  3°(B/E/F/I/J) │ → vencedor → Jogo 94 (casa)
Jogo 82  │ G1        vs  3°(A/E/H/I/J) │ → vencedor → Jogo 94 (fora)
Jogo 83  │ K2        vs  L2        │ → vencedor → Jogo 93 (fora)
Jogo 84  │ H1        vs  J2        │ → vencedor → Jogo 93 (casa)
Jogo 85  │ B1        vs  3°(E/F/G/I/J) │ → vencedor → Jogo 96 (casa)
Jogo 86  │ J1        vs  H2        │ → vencedor → Jogo 95 (casa)
Jogo 87  │ K1        vs  3°(D/E/I/J/L) │ → vencedor → Jogo 96 (fora)
Jogo 88  │ D2        vs  G2        │ → vencedor → Jogo 95 (fora)
```

## 🏟️ Chaveamento Completo — 16avas até a Final

```
16avas (5–12/jul)        8avas (15–18/jul)        Quartas (21–22/jul)     Semis (25–26/jul)    Final (29/jul)
─────────────────────    ─────────────────────    ──────────────────────  ────────────────────  ──────────────
Jogo 74 ──┐
          ├── Jogo 89 ──┐
Jogo 77 ──┘             │
                        ├── Jogo 97 ──┐
Jogo 73 ──┐             │             │
          ├── Jogo 90 ──┘             │
Jogo 75 ──┘                           ├── Jogo 101 ──┐
                                      │               │
Jogo 84 ──┐                           │               │
          ├── Jogo 93 ──┐             │               │
Jogo 83 ──┘             │             │               │
                        ├── Jogo 98 ──┘               │
Jogo 81 ──┐             │                             │
          ├── Jogo 94 ──┘                             ├── Jogo 103 🏆
Jogo 82 ──┘                                           │
                                                      │
Jogo 76 ──┐                                           │
          ├── Jogo 91 ──┐                             │
Jogo 78 ──┘             │                             │
                        ├── Jogo 99 ──┐               │
Jogo 79 ──┐             │             │               │
          ├── Jogo 92 ──┘             │               │
Jogo 80 ──┘                           ├── Jogo 102 ──┘
                                      │
Jogo 86 ──┐                           │
          ├── Jogo 95 ──┐             │
Jogo 88 ──┘             │             │
                        ├── Jogo 100 ─┘
Jogo 85 ──┐             │
          ├── Jogo 96 ──┘
Jogo 87 ──┘
```

## 🗓️ Calendário das Eliminatórias

| Fase | Jogos | Datas |
|---|---|---|
| **Fase de Grupos** | 1–72 | 11–27 jun 2026 |
| **16avas de Final** | 73–88 | 05–12 jul 2026 |
| **8avas de Final** | 89–96 | 15–18 jul 2026 |
| **Quartas de Final** | 97–100 | 21–22 jul 2026 |
| **Semifinal** | 101–102 | 25–26 jul 2026 |
| **Final** | 103 | 29 jul 2026 |

## 🔧 Endpoints Relevantes

| Endpoint | Função |
|---|---|
| `GET /api/classificacoes` | Classificação de todos os grupos (pontos, saldo, gols) |
| `POST /api/jogos/semear_todos_grupos` | Popula slots 1°/2° dos grupos concluídos nas 16avas |
| `POST /api/jogos/semear_terceiros` | Distribui os 8 melhores 3° nos slots disponíveis |
| `PUT /api/jogos/{id}/resultado` | Registra placar e aciona avanço automático no bracket |
| `PUT /api/jogos/{id}/times` | Atribui times manualmente (empates eliminatórios) |