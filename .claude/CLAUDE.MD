<h1 align="center">🏆 Bolão Copa do Mundo 2026 <br>
<img src="https://img.shields.io/badge/Claude-111827?style=for-the-badge&logo=claude&logoColor=orange" height="25" alt="claude"/>
</h1>

<p align="center">
    <img src="../img/claude.jpeg" alt="Claude Code logo" width="430">
</p>

Sistema de bolão para a Copa do Mundo 2026 — backend **FastAPI + PostgreSQL**, frontend **HTML/CSS/JS puro**, autenticação por **nome + senha com bcrypt**, orquestrado via **Docker Compose** com 3 containers (db, backend, frontend).

---

## 🧱 Stack Tecnológica

| Camada | Tecnologia | Versão | Função |
|--------|-----------|--------|--------|
| 🐍 Backend | Python + FastAPI | 3.12 / 0.115.0 | API REST + lógica de negócio |
| 🗄️ ORM | SQLAlchemy | 2.0.35 | Mapeamento objeto-relacional |
| ✅ Validação | Pydantic | 2.9.2 | Schemas de entrada/saída da API |
| 🐘 Banco | PostgreSQL | 16 | Persistência de dados |
| 🔒 Auth | passlib + bcrypt | 1.7.4 / <4.0.0 | Hash de senha (salt 12 rounds) |
| 🌐 Frontend | HTML5 + CSS3 + JS | — | Interface sem framework externo |
| 🚀 Servidor Web | Nginx | alpine | Serve estáticos + proxy reverso para `/api/*` |
| 🐳 Infra | Docker Compose | — | Orquestração dos 3 containers |

---

## 🗺️ Arquitetura

```
┌──────────────────────┐    HTTP     ┌───────────────────────┐    SQL     ┌──────────────────┐
│     Frontend         │ ──────────► │       Backend         │ ─────────► │  PostgreSQL 16   │
│  Nginx : 3000        │             │   FastAPI : 8000      │            │   bolao : 5433   │
│  (arquivos estáticos)│             │  (API REST + lógica)  │            │  (pgdata volume) │
└──────────────────────┘             └───────────────────────┘            └──────────────────┘
```

- **Nginx** serve os estáticos do frontend em `:3000` e faz proxy de `/api/*` → `backend:8000` (sem CORS)
- **FastAPI** expõe a API REST em `:8000`, só sobe após o healthcheck do banco (`pg_isready`) passar
- **PostgreSQL 16** persiste os dados na volume Docker `pgdata`

---

## 📁 Estrutura de Arquivos

```
Bolao-Copa-26/
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── principal.py             # Entrypoint — instancia o app via criar_app()
│       ├── modulo.py                # criar_app(): registra routers, CORS, etc.
│       ├── modelos.py               # Modelos SQLAlchemy (Fase, Time, Grupo, Jogo, Participante, Aposta)
│       ├── esquemas.py              # Schemas Pydantic (request/response bodies)
│       ├── banco.py                 # Engine + SessionLocal + get_db dependency
│       ├── popular.py               # Seed de dados (times, grupos, fases, jogos) — roda na inicialização
│       ├── apoio.py                 # Imprime coordenadas do mouse após 7s (helper para automação GUI)
│       ├── pesquisar_jogo.py        # Automação GUI: abre Chrome e pesquisa jogos da Copa
│       ├── auth/
│       │   ├── auth_controller.py   # Router: POST /api/auth/login
│       │   └── auth_service.py      # criar_hash_senha(), verificar_senha(), autenticar_participante()
│       ├── controller/
│       │   ├── jogos.py             # Rotas de jogos (GET, PUT resultado, PUT times, buscar, semear)
│       │   ├── apostas.py           # Rotas de apostas (GET, POST, PUT, DELETE)
│       │   └── placar.py            # Rota GET /api/placar (ranking financeiro)
│       ├── service/
│       │   ├── jogos.py             # Lógica de jogos, SEEDING_1_2, CHAVE_PROXIMO_JOGO, semear_terceiros
│       │   ├── apostas.py           # Cálculo de pontos por aposta
│       │   ├── placar.py            # Agregação do ranking com breakdown financeiro por fase
│       │   └── resultado_externo.py # Busca placar em openfootball/worldcup.json (cache 5 min)
│       └── color/
│           └── cores.py             # Constantes ANSI para colorir logs no terminal
│
├── frontend/
│   ├── html/index.html              # Página principal (ranking + apostas + jogos + classificação)
│   ├── css/style.css                # Estilos globais (dark-theme, tabelas, filtros, badges financeiros)
│   ├── js/app.js                    # Toda lógica client-side (fetch, render DOM, filtros, modais)
│   └── auth/
│       ├── html/login.html          # Formulário nome + senha
│       ├── css/login.css            # Estilos dark-theme do login
│       └── js/login.js              # fetch + localStorage + toast + redirect
│
├── docker/
│   ├── Dockerfile                   # Imagem do backend (Python 3.12 + pip install)
│   ├── docker-compose.yml           # Orquestração: db → backend → frontend
│   └── nginx.conf                   # Proxy /api/ → backend:8000, serve estáticos em /
│
├── api/
│   └── openapi.yml                  # Spec OpenAPI 3.1 (gerado pelo FastAPI)
│
└── docs/
    ├── API.md                       # Documentação técnica detalhada dos endpoints
    └── TRACKER_COLOCADOS.md         # Tracker de apostas colocadas
```

---

## 🗃️ Modelos de Dados

| Modelo | Tabela | Descrição |
|--------|--------|-----------|
| **Fase** | `fases` | Grupos, Oitavas, Quartas, Semis, Final — com peso de pontuação por fase (`valor`) |
| **Time** | `times` | Seleções com nome e bandeira emoji (ex: 🇧🇷) |
| **Grupo** | `grupos` | Grupos A–L da fase de grupos |
| **Jogo** | `jogos` | Partidas com times, data, local, placar (`gols_casa`/`gols_fora`) e status `encerrado` |
| **Participante** | `participantes` | Apostadores — `senha_hash` com bcrypt saltround 12 |
| **Aposta** | `apostas` | Palpite de placar por participante/jogo — `pontos` calculados ao encerrar o jogo |

> ⚠️ `UniqueConstraint("id_participante", "id_jogo")` em `apostas` — um participante aposta **uma vez** por jogo.

---

## 🌐 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/api/auth/login` | Autentica `{ nome, senha }` → `{ id, nome }` via bcrypt verify |
| `GET` | `/api/jogos` | Lista jogos — filtros `?id_fase=` e `?id_grupo=` |
| `GET` | `/api/jogos/{id}` | Detalha um jogo |
| `PUT` | `/api/jogos/{id}/resultado` | Registra placar, calcula pontos e avança vencedor no bracket |
| `PUT` | `/api/jogos/{id}/times` | Atualiza times do jogo (fases eliminatórias) |
| `GET` | `/api/jogos/{id}/buscar_resultado` | Busca placar na fonte externa (openfootball) com cache 5 min |
| `POST` | `/api/jogos/recalcular_tudo` | Re-aplica pontuação em todos os jogos encerrados |
| `POST` | `/api/jogos/semear_todos_grupos` | Semeia 1° e 2° de todos os grupos concluídos nos slots das 16avas |
| `POST` | `/api/jogos/semear_terceiros` | Distribui os 8 melhores 3° colocados nas 16avas (matching bipartido) |
| `GET` | `/api/apostas` | Lista apostas — filtros `?id_participante=` e `?id_jogo=` |
| `POST` | `/api/apostas` | Cria aposta `{ id_participante, id_jogo, palpite_casa, palpite_fora }` |
| `PUT` | `/api/apostas/{id}` | Atualiza palpite (somente antes do encerramento do jogo) |
| `DELETE` | `/api/apostas/{id}` | Remove aposta |
| `GET` | `/api/placar` | Ranking com breakdown financeiro por fase (saldo, ganho, devido, acertos) |
| `GET` | `/api/classificacoes` | Classificação dos grupos (V=3, E=1, D=0 — critérios FIFA) |
| `GET` | `/api/fases` | Lista fases ordenadas |
| `GET` | `/api/times` | Lista seleções ordenadas por nome |
| `GET` | `/api/grupos` | Lista grupos |
| `GET` | `/api/participantes` | Lista participantes |
| `GET` | `/saude` | Health check `{ "status": "running❤️🏥" }` |

> 📖 Swagger UI: **http://localhost:8000/docs** | 📄 Spec: [`api/openapi.yml`](../api/openapi.yml) | 📋 Técnico: [`docs/API.md`](../docs/API.md)

---

## 🏆 Sistema de Pontuação

| Resultado | Saldo |
|-----------|-------|
| **Acertou o placar exato** (único acertador) | `+ R$ valor_fase × nº de erros` (fica com o bolo inteiro) |
| **Acertou o placar exato** (múltiplos acertadores) | `+ R$ (valor_fase × nº de erros) ÷ nº acertadores` (prêmio dividido) |
| **Errou** (mas alguém acertou) | `- R$ valor_fase` |
| **Ninguém acertou** | `= R$ 0,00` (jogo neutro) |

| Fase | Valor por jogo |
|------|---------------|
| Fase de Grupos | R$ 1,00 |
| 16avos / Oitavas / Quartas | R$ 2,00 |
| Semifinal | R$ 5,00 |
| Final | R$ 10,00 |

> Se ninguém acertar o placar exato, o jogo é **neutro** — ninguém ganha nem perde. Quando múltiplos acertam, o prêmio total é dividido igualmente.

---

## ⚙️ Chaveamento Eliminatório

### Seeding: Grupos → 16avas

Ao registrar o resultado do **último jogo de um grupo**, o backend classifica 1° e 2° automaticamente (critérios: pontos → saldo de gols → gols marcados) e preenche os slots nas 16avas via `SEEDING_1_2` em `service/jogos.py`.

Os 8 melhores **3° colocados** são distribuídos após todos os 12 grupos encerrarem via `POST /api/jogos/semear_terceiros` (matching bipartido, bracket FIFA).

| Ação | Trigger |
|------|---------|
| Semear 1° e 2° de um grupo | Automático ao registrar o último jogo do grupo |
| Semear grupos já concluídos | `POST /api/jogos/semear_todos_grupos` (ou botão 🌱) |
| Semear 8 melhores 3° colocados | `POST /api/jogos/semear_terceiros` (ou botão 🥉) |
| Corrigir slot pontual | `PUT /api/jogos/{id}/times` |

### Avanço automático no mata-mata

Ao registrar resultado de um jogo eliminatório, o vencedor avança automaticamente via `CHAVE_PROXIMO_JOGO` em `service/jogos.py`:

| Rodada | Jogos | Avança para |
|--------|-------|-------------|
| 16avos | jg 73–88 | 8avos (jg 89–96) |
| 8avos | jg 89–96 | Quartas (jg 97–100) |
| Quartas | jg 97–100 | Semis (jg 101–102) |
| Semis | jg 101–102 | Final (jg 103) |

> Em caso de empate, o slot não é preenchido automaticamente — usar `PUT /api/jogos/{id}/times`.

---

## 🔒 Autenticação

- Login via **nome + senha** — sessão guardada no `localStorage` do browser (sem JWT)
- Senhas hasheadas com **bcrypt saltround 12** via `passlib[bcrypt]==1.7.4`
- `bcrypt` fixado em `>=3.1.0,<4.0.0` — versões ≥ 4 são incompatíveis com passlib 1.7.4
- Senha padrão do seed: `03070203` (aplicada em `popular.py`)
- Hash armazenado em `participantes.senha_hash VARCHAR(100)`

```
POST /api/auth/login  { nome, senha }
  └─► auth_controller.py
        └─► auth_service.autenticar_participante(bd, nome, senha)
              └─► bcrypt.verify(senha, participante.senha_hash)
                    ├─► ✅ 200  { id, nome }  →  localStorage.participante_auth
                    └─► ❌ 401  "Nome ou senha incorretos."
```

Guard em `index.html`: redireciona para `/auth/login.html` se não autenticado. Toast "Bem-vindo de volta, {nome}!" ao entrar (flag `recem_logado` no localStorage).

---

## 🌍 Resultado Externo (`service/resultado_externo.py`)

Consulta o feed público `openfootball/worldcup.json` para obter placares reais. Cache em memória com validade de **5 minutos** (`VALIDADE_CACHE`).

```
[Botão "🌐 Buscar" no modal]
  GET /api/jogos/{id}/buscar_resultado
    └─► resultado_externo.buscar_resultado(numero)
          ├─► cache válido? → retorna imediatamente
          └─► cache expirado → GET openfootball GitHub JSON
                └─► mapeia índice+1 → número do jogo
                      └─► { gols_casa, gols_fora }
  → preenche campos do modal (não salva até o usuário clicar ✅ Salvar)
```

> ⚠️ O jogo de 3° lugar é excluído do mapeamento para manter a numeração compatível com o banco.

---

## 🖥️ Frontend

### `js/app.js` — funções principais

| Função | O que faz |
|--------|-----------|
| `recalcularPontuacoes()` | `POST /api/jogos/recalcular_tudo` → recarrega ranking |
| `buscarResultadoExterno()` | `GET /api/jogos/{id}/buscar_resultado` → preenche modal |
| `filtrarPorData()` / `filtrarHoje()` / `limparFiltros()` | Filtros de data na listagem de jogos |
| `renderizarPlacar()` | Ranking + tabelas por fase (acertos, ganho, a pagar, saldo) |
| `semearGrupos()` | `POST /api/jogos/semear_todos_grupos` → recarrega jogos |
| `semearTerceiros()` | `POST /api/jogos/semear_terceiros` → recarrega jogos |

### `docker/nginx.conf`

Serve estáticos em `:3000` e faz proxy de `/api/*` → `http://backend:8000`. O browser só conhece porta 3000 — sem CORS entre frontend e backend.

---

## ⚙️ Containers Docker

| Container | Imagem | Porta | Healthcheck | Depende de |
|-----------|--------|-------|-------------|------------|
| `bolao-db` | `postgres:16` | 5433→5432 | `pg_isready` a cada 5s | — |
| `bolao-backend` | Dockerfile local | 8000→8000 | — | `bolao-db` (healthcheck OK) |
| `bolao-frontend` | `nginx:alpine` | 3000→80 | — | `bolao-backend` |

---

## 🚀 Como Rodar

```bash
# Sobe tudo com rebuild
docker compose -f docker/docker-compose.yml up --build

# Background
docker compose -f docker/docker-compose.yml up -d --build

# Parar (mantém volume)
docker compose -f docker/docker-compose.yml down

# Reset total do banco (apaga volume)
docker compose -f docker/docker-compose.yml down -v

# Logs em tempo real
docker compose -f docker/docker-compose.yml logs -f backend
```

| Serviço | URL |
|---------|-----|
| 🌐 Frontend | http://localhost:3000 |
| ⚡ Swagger UI | http://localhost:8000/docs |
| 🐘 Banco | localhost:5433 — db `bolao_copa26`, user `bolao` |

### Backend direto (dev)

```bash
pip install -r backend/requirements.txt
uvicorn backend.app.principal:app --reload
```

---

## 🏟️ Contexto Copa 2026

- **48 seleções**, **12 grupos** (A–L), 4 times por grupo, 6 jogos por grupo
- Gap de **8 dias** entre fim dos grupos e início das oitavas

| Fase | Slug | Times | Jogos |
|------|------|-------|-------|
| Fase de Grupos | `grupos` | 48 | 72 |
| 16avos de Final | `dezesseis_avos` | 16 | 16 |
| Oitavas de Final | `oitavas` | 16 | 8 |
| Quartas de Final | `quartas` | 8 | 4 |
| Semifinal | `semi` | 4 | 2 |
| Disputa 3° Lugar | `terceiro` | 2 | 1 |
| Final | `final` | 2 | 1 |

---

## 📦 Dependências Python

```
fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
pydantic==2.9.2
python-dotenv==1.0.1
bcrypt>=3.1.0,<4.0.0
passlib[bcrypt]==1.7.4
```
