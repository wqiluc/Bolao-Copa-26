<h1 align="center">API — Bolão Copa do Mundo 2026 🏆⚽<br>
<img src="https://img.shields.io/badge/FastAPI-111827?style=for-the-badge&logo=fastapi&logoColor=009688"/>
<img src="https://img.shields.io/badge/REST-111827?style=for-the-badge&logo=swagger&logoColor=cyan"/>
</h1>

<p align="center">
  Documentação técnica da API REST que computa jogos, gols e pontuações do bolão.
</p>

<h2 align="center">📋 Visão Geral <br>
<img src="https://img.shields.io/badge/Overview-111827?style=flat-square&logo=swagger&logoColor=cyan"/>
</h2>

A API é construída com **FastAPI** e exposta na porta `8000`. Toda a lógica de negócio vive nos módulos `service/`, que são chamados pelos roteadores em `controller/`. A documentação interativa (Swagger UI) fica disponível em `http://localhost:8000/docs`.

| Campo | Valor |
|---|---|
| **Base URL** | `http://localhost:8000` |
| **Formato** | JSON (`Content-Type: application/json`) |
| **Documentação interativa** | `GET /docs` (Swagger UI) |
| **Spec OpenAPI** | [`api/openapi.yml`](../api/openapi.yml) |

---

<h2 align="center">🎯 Endpoints de Jogos <br>
<img src="https://img.shields.io/badge/Controller-jogos.py-009688?style=flat-square&logo=fastapi&logoColor=009688"/>
</h2>

### `GET /api/jogos`

Lista todos os jogos. Aceita filtros opcionais por fase e grupo.

| Query param | Tipo | Descrição |
|---|---|---|
| `id_fase` | `int` (opcional) | Filtra por fase (ex.: `1` = grupos, `2` = 16avos) |
| `id_grupo` | `int` (opcional) | Filtra pelo grupo (ex.: `1` = Grupo A) |

**Resposta** `200 OK` — array de `JogoSaída`:

```json
[
  {
    "id": 1,
    "numero": 1,
    "data": "2026-06-11T18:00:00",
    "fase": { "id": 1, "nome": "Fase de Grupos", "slug": "grupos", "ordem": 1, "valor": 1.0 },
    "grupo": { "id": 1, "nome": "Grupo A" },
    "time_casa": { "id": 3, "nome": "México", "bandeira": "🇲🇽" },
    "time_fora": { "id": 12, "nome": "Canadá", "bandeira": "🇨🇦" },
    "descricao": null,
    "local": "SoFi Stadium, Los Angeles",
    "gols_casa": null,
    "gols_fora": null,
    "encerrado": false
  }
]
```

---

### `GET /api/jogos/{id}`

Retorna um jogo específico.

| Path param | Tipo | Descrição |
|---|---|---|
| `id` | `int` | ID do jogo no banco |

**Resposta** `200 OK` — objeto `JogoSaída`  
**Resposta** `404 Not Found` — `{ "detail": "Jogo não encontrado" }`

---

### `PUT /api/jogos/{id}/resultado`

**Endpoint central da computação.** Registra o placar real de um jogo, recalcula os pontos de todas as apostas daquele jogo e avança o vencedor no chaveamento eliminatório (se aplicável).

| Path param | Tipo | Descrição |
|---|---|---|
| `id` | `int` | ID do jogo |

**Corpo da requisição:**

```json
{
  "gols_casa": 2,
  "gols_fora": 1
}
```

**O que acontece internamente (fluxo completo):**

```
PUT /resultado
    │
    ├─ 1. Persiste gols_casa, gols_fora e encerrado=True no banco
    │
    ├─ 2. recalcular_apostas(jogo)
    │       ├─ Coleta ganhadores (palpite == placar real)
    │       ├─ Se nenhum acertou → pontos = 0 para todos (neutro)
    │       └─ Se há acertadores:
    │               ├─ perdedor → pontos = −valor_fase
    │               └─ ganhador → pontos = +(valor_fase × nº_perdedores / nº_ganhadores)
    │
    └─ 3. avancar_vencedor(jogo)   [só em jogos eliminatórios]
            ├─ Determina vencedor (gols_casa > gols_fora → time_casa, senão time_fora)
            ├─ Consulta CHAVE_PROXIMO_JOGO para saber qual jogo recebe o vencedor
            └─ Preenche id_time_casa ou id_time_fora do próximo jogo
```

**Resposta** `200 OK` — objeto `JogoSaída` atualizado  
**Resposta** `404 Not Found` — jogo não encontrado

---

### `PUT /api/jogos/{id}/times`

Atualiza os times de um jogo. Usado manualmente em fases eliminatórias quando há empate no tempo regulamentar (pênaltis, prorrogação).

**Corpo:**

```json
{
  "id_time_casa": 7,
  "id_time_fora": 15
}
```

**Resposta** `200 OK` — objeto `JogoSaída`

---

### `GET /api/jogos/{id}/buscar_resultado`

Busca o placar real de um jogo na fonte externa [openfootball/worldcup.json](https://github.com/openfootball/worldcup.json). Implementa **cache em memória com TTL de 5 minutos** para evitar chamadas repetidas à fonte.

**Resposta** `200 OK`:

```json
{
  "gols_casa": 2,
  "gols_fora": 0
}
```

**Resposta** `404 Not Found` — resultado ainda não disponível na fonte externa

> **Importante:** este endpoint apenas **retorna** o placar. Ele não persiste nada no banco nem recalcula pontos. Para salvar o resultado, use `PUT /api/jogos/{id}/resultado` após confirmar os gols.

---

### `POST /api/jogos/recalcular_tudo`

Re-aplica a lógica de pontuação em **todos** os jogos encerrados. Útil para corrigir pontuações após mudança nas regras ou ajuste manual de placar.

**Resposta** `200 OK`:

```json
{
  "recalculados": 48
}
```

---

<h2 align="center">🎲 Endpoints de Apostas <br>
<img src="https://img.shields.io/badge/Controller-apostas.py-009688?style=flat-square&logo=fastapi&logoColor=009688"/>
</h2>

### `GET /api/apostas`

Lista apostas com filtros opcionais.

| Query param | Tipo | Descrição |
|---|---|---|
| `id_participante` | `int` (opcional) | Filtra por participante |
| `id_jogo` | `int` (opcional) | Filtra por jogo |

**Resposta** `200 OK` — array de `ApostaSaída`:

```json
[
  {
    "id": 42,
    "participante": { "id": 2, "nome": "Lucas" },
    "jogo": { ... },
    "palpite_casa": 2,
    "palpite_fora": 1,
    "valor": 1.0,
    "pontos": 3.0
  }
]
```

> `pontos > 0` → acertou o placar exato e ganhou  
> `pontos < 0` → errou e deve pagar  
> `pontos = 0` → jogo neutro (ninguém acertou)

---

### `POST /api/apostas`

Cria uma aposta. Só é aceita se o jogo **não estiver encerrado**.

```json
{
  "id_participante": 2,
  "id_jogo": 1,
  "palpite_casa": 2,
  "palpite_fora": 1
}
```

O campo `valor` é preenchido automaticamente com `fase.valor` do jogo apostado.

**Resposta** `201 Created` — objeto `ApostaSaída`  
**Resposta** `400 Bad Request` — jogo encerrado ou inválido  
**Resposta** `409 Conflict` — aposta duplicada (mesma combinação participante+jogo)

---

### `PUT /api/apostas/{id}`

Atualiza palpite de uma aposta existente. Só permitido enquanto o jogo não estiver encerrado.

```json
{
  "palpite_casa": 1,
  "palpite_fora": 0
}
```

**Resposta** `200 OK` — objeto `ApostaSaída` atualizado  
**Resposta** `400 Bad Request` — jogo já encerrado

---

### `DELETE /api/apostas/{id}`

Remove uma aposta. Só permitido enquanto o jogo não estiver encerrado.

**Resposta** `204 No Content`  
**Resposta** `400 Bad Request` — jogo já encerrado

---

<h2 align="center">🏆 Endpoint de Placar <br>
<img src="https://img.shields.io/badge/Controller-placar.py-009688?style=flat-square&logo=fastapi&logoColor=009688"/>
</h2>

### `GET /api/placar`

Retorna o ranking geral de participantes com **breakdown financeiro por fase** — quantos acertaram, quanto ganharam, quanto devem e saldo total.

**Resposta** `200 OK` — array de `PlacarParticipante`, ordenado por `saldo_total DESC`, depois por `acertos_exatos DESC`:

```json
[
  {
    "participante": { "id": 2, "nome": "Lucas" },
    "saldo_total": 12.50,
    "total_ganho": 15.00,
    "total_devido": 2.50,
    "acertos_exatos": 7,
    "por_fase": [
      {
        "fase": { "id": 1, "nome": "Fase de Grupos", "valor": 1.0, ... },
        "saldo": 4.00,
        "ganho": 5.00,
        "devido": 1.00,
        "acertos": 4
      },
      {
        "fase": { "id": 2, "nome": "16avos", "valor": 2.0, ... },
        "saldo": 8.50,
        "ganho": 10.00,
        "devido": 1.50,
        "acertos": 3
      }
    ]
  }
]
```

---

<h2 align="center">📦 Endpoints Auxiliares</h2>

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/fases` | Lista fases ordenadas por `ordem` |
| `GET` | `/api/times` | Lista seleções ordenadas por `nome` |
| `GET` | `/api/grupos` | Lista grupos (A–L) |
| `GET` | `/api/participantes` | Lista participantes do bolão |
| `GET` | `/api/classificacoes` | Classificação de todos os grupos (V=3, E=1, D=0) |
| `GET` | `/saude` | Health check — `{ "status": "ok" }` |

---

<h2 align="center">⚙️ Lógica de Computação de Pontos <br>
<img src="https://img.shields.io/badge/Service-jogos.py-3776AB?style=flat-square&logo=python&logoColor=3776AB"/>
</h2>

A função `recalcular_apostas` em [`service/jogos.py`](../backend/app/service/jogos.py) é o núcleo do sistema de pontuação. Ela é invocada tanto ao registrar um resultado quanto pelo endpoint `/recalcular_tudo`.

```python
# Pseudocódigo da regra de negócio
ganhadores = [a for a in apostas if a.palpite == placar_real]
perdedores  = [a for a in apostas if a not in ganhadores]

if not (ganhadores):
    # Ninguém acertou → jogo neutro
    for a in apostas: a.pontos = 0
else:
    premio = round(valor_fase * len(perdedores) / len(ganhadores), 2)
    for a in ganhadores: a.pontos = +premio
    for a in perdedores: a.pontos = -valor_fase
```

**Exemplos numéricos com `valor_fase = R$ 1,00` e 4 apostadores:**

| Cenário | Acertadores | Errados | Pontos do ganhador | Pontos do perdedor |
|---|---|---|---|---|
| 1 acertou | 1 | 3 | `+3,00` | `−1,00` |
| 2 acertaram | 2 | 2 | `+1,00` | `−1,00` |
| 4 acertaram | 4 | 0 | `+0,00` | — |
| Ninguém acertou | 0 | 4 | — | `0,00` (neutro) |

---

<h2 align="center">⛓️ Chaveamento Eliminatório <br>
<img src="https://img.shields.io/badge/Service-CHAVE__PROXIMO__JOGO-3776AB?style=flat-square&logo=python&logoColor=3776AB"/>
</h2>

Ao registrar o resultado de um jogo eliminatório (jogos 73–103), a função `avancar_vencedor` preenche automaticamente o slot `casa` ou `fora` do próximo jogo conforme o mapeamento `CHAVE_PROXIMO_JOGO`:

```
16avos  (jg 73–88)  →  8avos  (jg 89–96)
8avos   (jg 89–96)  →  Quartas (jg 97–100)
Quartas (jg 97–100) →  Semis  (jg 101–102)
Semis   (jg 101–102)→  Final  (jg 103)
```

> Em caso de **empate** no tempo regulamentar, o slot não é preenchido automaticamente.  
> Use `PUT /api/jogos/{id}/times` para atribuir os times manualmente.

---

<h2 align="center">🌐 Fluxo do "Buscar Resultado" <br>
<img src="https://img.shields.io/badge/Service-resultado__externo.py-3776AB?style=flat-square&logo=python&logoColor=3776AB"/>
</h2>

O botão "🌐 Buscar" no frontend percorre três camadas antes de preencher os campos de gols:

```
Frontend (buscarResultadoExterno)
    │
    └─ GET /api/jogos/{id}/buscar_resultado
            │
            ├─ 1. Busca o jogo no banco pelo id
            ├─ 2. Extrai jogo.numero (sequencial da Copa, não o ID do banco)
            └─ 3. resultado_externo.buscar_resultado(numero)
                        │
                        ├─ Cache válido? → retorna da memória
                        └─ Cache expirado/vazio?
                                │
                                ├─ GET openfootball/worldcup.json
                                ├─ Filtra jogo de 3º lugar
                                ├─ Indexa filtrados por ordem: jogo 1, 2, 3...
                                └─ Retorna score.ft = [gols_casa, gols_fora]
```

**Fonte dos dados:** [`openfootball/worldcup.json`](https://github.com/openfootball/worldcup.json) — JSON público mantido pela comunidade com os resultados da Copa 2026.

**Cache em memória (TTL = 300 s):** todos os placares são baixados de uma vez e ficam armazenados em `resultado_externo.cache`. Uma nova requisição à fonte só ocorre após 5 minutos ou se o processo restartar. Isso evita rate-limit e latência em cascata quando vários admins clicam "Buscar" ao mesmo tempo.

**Por que `jogo.numero` e não `jogo.id`?** O `id` é chave interna do banco; o `numero` é a posição sequencial do jogo na competição (1 = primeiro jogo da fase de grupos, 72 = último da fase de grupos, 73 = primeiro das oitavas, etc.), que coincide com o índice do JSON externo. O jogo de 3º lugar é excluído dessa contagem porque o bolão não o contempla.

**O buscar não salva nada.** Ele apenas preenche os campos do modal no frontend. O admin precisa confirmar e clicar em "Salvar", que dispara `PUT /api/jogos/{id}/resultado` → persiste no banco → recalcula apostas → avança chaveamento (se eliminatório).

**Fluxo completo para registrar um resultado via UI:**

```
1. Admin abre modal de resultado de um jogo
2. Clica "🌐 Buscar"  →  GET /buscar_resultado  →  preenche campos
3. Confere o placar
4. Clica "Salvar"     →  PUT /resultado         →  persiste + recalcula
```

---

<h2 align="center">🗂️ Schemas Pydantic <br>
<img src="https://img.shields.io/badge/Pydantic-esquemas.py-E92063?style=flat-square&logo=pydantic&logoColor=E92063"/>
</h2>

Definidos em [`backend/app/esquemas.py`](../backend/app/esquemas.py):

| Schema | Direção | Campos principais |
|---|---|---|
| `JogoSaida` | Saída | `id`, `numero`, `data`, `fase`, `grupo`, `time_casa`, `time_fora`, `gols_casa`, `gols_fora`, `encerrado` |
| `ResultadoJogo` | Entrada | `gols_casa`, `gols_fora` |
| `AtualizarTimesJogo` | Entrada | `id_time_casa`, `id_time_fora` |
| `ApostaEntrada` | Entrada | `id_participante`, `id_jogo`, `palpite_casa`, `palpite_fora` |
| `AtualizarAposta` | Entrada | `palpite_casa`, `palpite_fora` |
| `ApostaSaida` | Saída | `id`, `participante`, `jogo`, `palpite_casa`, `palpite_fora`, `valor`, `pontos` |
| `PlacarParticipante` | Saída | `participante`, `saldo_total`, `total_ganho`, `total_devido`, `acertos_exatos`, `por_fase` |
| `PlacarFase` | Saída | `fase`, `saldo`, `ganho`, `devido`, `acertos` |

---

> 📖 Documentação interativa disponível em **http://localhost:8000/docs** (Swagger UI)  
> 📄 Spec completo em [`api/openapi.yml`](../api/openapi.yml) — OpenAPI 3.1, gerado diretamente do FastAPI
