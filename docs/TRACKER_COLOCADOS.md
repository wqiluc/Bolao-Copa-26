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

> Jogos de 28 jun a 03 jul 2026 · Fonte: `CHAVE_PROXIMO_JOGO` em [`backend/app/service/jogos.py`](../backend/app/service/jogos.py)

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
16avas (28/jun–3/jul)    8avas (4–7/jul)          Quartas (9–10/jul)      Semis (14–15/jul)    Final (19/jul)
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
| **16avas de Final** | 73–88 | 28 jun–03 jul 2026 |
| **8avas de Final** | 89–96 | 04–07 jul 2026 |
| **Quartas de Final** | 97–100 | 09–10 jul 2026 |
| **Semifinal** | 101–102 | 14–15 jul 2026 |
| **Final** | 103 | 19 jul 2026 |

## 🎯 Estado Atual das 16avas — 25/06/2026

> Atualizado com pesquisa em tempo real. ✅ = confronto/time confirmado · ⏳ = aguardando rodada final · — = adversário indefinido

### Classificados por Grupo (fase de grupos)

| Grupo | 1° Lugar | 2° Lugar | Status |
|---|---|---|---|
| **A** | 🇲🇽 México | 🇿🇦 África do Sul | ✅ Encerrado (24/jun) |
| **B** | 🇨🇭 Suíça | 🇨🇦 Canadá | ✅ Encerrado (24/jun) |
| **C** | 🇧🇷 Brasil | 🇲🇦 Marrocos | ✅ Encerrado (24/jun) |
| **D** | 🇺🇸 EUA | ⏳ 🇦🇺 Austrália (GD +0) ou 🇵🇾 Paraguai (GD −3) | ⏳ Final: 25/jun 22h — Aus vs Par |
| **E** | 🇩🇪 Alemanha | ⏳ 🇨🇮 Costa do Marfim (3pts, favorita) | ⏳ Final: 25/jun 16h — Ale vs Equ, CMF vs Cur |
| **F** | ⏳ 🇳🇱 Holanda (4pts, favorita F1) | ⏳ 🇯🇵 Japão (4pts) ou 🇸🇪 Suécia (3pts) | ⏳ Final: 25/jun 19h — Jap vs Sue, Hol vs Tun |
| **G** | ⏳ 🇪🇬 Egito (4pts, líder) ou 🇧🇪 Bélgica (2pts) | ⏳ ? | ⏳ Final: 26/jun |
| **H** | 🇪🇸 Espanha | 🇺🇾 Uruguai | ✅ Encerrado |
| **I** | ⏳ França ou Noruega | ⏳ Noruega ou França | ⏳ Final: 26/jun (Fra vs Nor) |
| **J** | 🇦🇷 Argentina | ⏳ Áustria ou Argélia | ⏳ Final: 27/jun (Aut vs Alg) |
| **K** | ⏳ Colômbia ou Portugal | ⏳ Portugal ou Colômbia | ⏳ Final: 27/jun (Col vs Por) |
| **L** | ⏳ Inglaterra ou Gana | ⏳ ? | ⏳ Final: 27/jun (Ing vs Gana, Cro vs Pan) |

> 3° colocados: 🇧🇦 Bósnia (Grupo B) é o primeiro 3° confirmado. Os demais slots serão definidos após o encerramento de todos os grupos.

---

### ⚔️ Chaveamento das 16avas — Times Confirmados

> `✅` = ambos os times definidos · `🔸` = um time definido · `⏳` = aguardando grupos

```
Jogo 73  ✅ │ 🇿🇦 África do Sul   vs  🇨🇦 Canadá          │ → Jogo 90
Jogo 74  🔸 │ 🇩🇪 Alemanha        vs  — (3°)              │ → Jogo 89
Jogo 75  🔸 │ — (F1)              vs  🇲🇦 Marrocos         │ → Jogo 90
Jogo 76  🔸 │ 🇧🇷 Brasil          vs  — (F2)              │ → Jogo 91
Jogo 77  ⏳ │ — (I1: Fra/Nor)     vs  — (3°)              │ → Jogo 89
Jogo 78  ⏳ │ — (E2)              vs  — (I2: Nor/Fra)     │ → Jogo 91
Jogo 79  🔸 │ 🇲🇽 México          vs  — (3°)              │ → Jogo 92
Jogo 80  ⏳ │ — (L1)              vs  — (3°)              │ → Jogo 92
Jogo 81  🔸 │ 🇺🇸 EUA             vs  — (3°)              │ → Jogo 94
Jogo 82  ⏳ │ — (G1)              vs  — (3°)              │ → Jogo 94
Jogo 83  ⏳ │ — (K2)              vs  — (L2)              │ → Jogo 93
Jogo 84  🔸 │ 🇪🇸 Espanha         vs  — (J2)              │ → Jogo 93
Jogo 85  🔸 │ 🇨🇭 Suíça           vs  — (3°)              │ → Jogo 96
Jogo 86  ✅ │ 🇦🇷 Argentina       vs  🇺🇾 Uruguai          │ → Jogo 95
Jogo 87  ⏳ │ — (K1)              vs  — (3°)              │ → Jogo 96
Jogo 88  ⏳ │ — (D2)              vs  — (G2)              │ → Jogo 95
```

**Confrontos já definidos:**
- 🇿🇦 **África do Sul vs 🇨🇦 Canadá** (Jogo 73 · 05/jul)
- 🇦🇷 **Argentina vs 🇺🇾 Uruguai** (Jogo 86 · 11/jul) — clássico sul-americano confirmado!

**Times com slot definido mas sem adversário:**
- 🇩🇪 Alemanha (Jogo 74 casa) · 🇲🇦 Marrocos (Jogo 75 fora) · 🇧🇷 Brasil (Jogo 76 casa)
- 🇲🇽 México (Jogo 79 casa) · 🇺🇸 EUA (Jogo 81 casa) · 🇪🇸 Espanha (Jogo 84 casa) · 🇨🇭 Suíça (Jogo 85 casa)

---

## 🔧 Endpoints Relevantes

| Endpoint | Função |
|---|---|
| `GET /api/classificacoes` | Classificação de todos os grupos (pontos, saldo, gols) |
| `POST /api/jogos/semear_todos_grupos` | Popula slots 1°/2° dos grupos concluídos nas 16avas |
| `POST /api/jogos/semear_terceiros` | Distribui os 8 melhores 3° nos slots disponíveis |
| `PUT /api/jogos/{id}/resultado` | Registra placar e aciona avanço automático no bracket |
| `PUT /api/jogos/{id}/times` | Atribui times manualmente (empates eliminatórios) |