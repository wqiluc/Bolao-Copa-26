<h1 align="center"> Bolão Copa do Mundo 2026 🏆⚽🌎 <br>
<img src="./img/logofifa.jpeg" width="420" alt="Logo FIFA 2026"/></h1>

<h2 align="center">💻⛏️ Tecnologias e Ferramentas Utilizadas:</h2>
<p align="center">
  <img src="https://img.shields.io/badge/Python-111827?style=for-the-badge&logo=python&logoColor=3776AB" height="25" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-111827?style=for-the-badge&logo=fastapi&logoColor=009688" height="25" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-111827?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00" height="25" alt="SQLAlchemy"/>
  <img src="https://img.shields.io/badge/Pydantic-111827?style=for-the-badge&logo=pydantic&logoColor=E92063" height="25" alt="Pydantic"/>
  <img src="https://img.shields.io/badge/PostgreSQL-111827?style=for-the-badge&logo=postgresql&logoColor=white" height="25" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Docker-111827?style=for-the-badge&logo=docker&logoColor=2496ED" height="25" alt="Docker"/>
  <img src="https://img.shields.io/badge/Nginx-111827?style=for-the-badge&logo=nginx&logoColor=009639" height="25" alt="Nginx"/>
  <img src="https://img.shields.io/badge/HTML5-111827?style=for-the-badge&logo=html5&logoColor=E34F26" height="25" alt="HTML5"/>
  <img src="https://img.shields.io/badge/-CSS-111827?style=flat-square&logo=css&logoColor=663399" height="25" alt="CSS3"/>
  <img src="https://img.shields.io/badge/JavaScript-111827?style=for-the-badge&logo=javascript&logoColor=F7DF1E" height="25" alt="JavaScript"/> <br>
  <img src="https://img.shields.io/badge/Git-111827?style=for-the-badge&logo=git&logoColor=F05032" height="25" alt="Git"/>
  <img src="https://img.shields.io/badge/GitHub-111827?style=for-the-badge&logo=github&logoColor=white" height="25" alt="GitHub"/>
  <img src="https://img.shields.io/badge/GitHub_Desktop-111827?style=for-the-badge&logo=github&logoColor=purple" height="25" alt="GitHub"/>
</p>

<h2 align="center">🏰 Arquitetura do Projeto</h2>

<pre>
Bolao-Copa-26⚽/
├── backend <img src="https://img.shields.io/badge/Python-111827?style=flat&logo=python&logoColor=3776AB" height="18"/> <img src="https://img.shields.io/badge/-FastAPI-111827?style=flat&logo=fastapi&logoColor=009688" height="18"/> <img src="https://img.shields.io/badge/-SQLAlchemy-111827?style=flat&logo=sqlalchemy&logoColor=D71F00" height="18"/>/
│   ├── app <img src="https://img.shields.io/badge/src-8B0000?style=flat&logo=python&logoColor=white" height="18"/>/
│   │   ├── controller <img src="https://img.shields.io/badge/-Controller-111827?style=flat&logo=fastapi&logoColor=009688" height="18"/>/
│   │   │   ├── jogos.py <img src="https://img.shields.io/badge/Roteador_Jogos-111827?style=flat&logo=python&logoColor=F7DF1E" height="18"/>
│   │   │   ├── apostas.py <img src="https://img.shields.io/badge/Roteador_Apostas-111827?style=flat&logo=python&logoColor=F7DF1E" height="18"/>
│   │   │   └── placar.py <img src="https://img.shields.io/badge/Roteador_Placar-111827?style=flat&logo=python&logoColor=F7DF1E" height="18"/>
│   │   ├── service <img src="https://img.shields.io/badge/-Service-111827?style=flat&logo=python&logoColor=3776AB" height="18"/>/
│   │   │   ├── jogos.py <img src="https://img.shields.io/badge/Service_Jogos-111827?style=flat&logo=python&logoColor=3776AB" height="18"/>
│   │   │   ├── apostas.py <img src="https://img.shields.io/badge/Service_Apostas-111827?style=flat&logo=python&logoColor=3776AB" height="18"/>
│   │   │   └── placar.py <img src="https://img.shields.io/badge/Service_Placar-111827?style=flat&logo=python&logoColor=3776AB" height="18"/>
│   │   ├── banco.py <img src="https://img.shields.io/badge/Conexão_BD-111827?style=flat&logo=postgresql&logoColor=white" height="18"/>
│   │   ├── esquemas.py <img src="https://img.shields.io/badge/Pydantic_Schemas-111827?style=flat&logo=pydantic&logoColor=E92063" height="18"/>
│   │   ├── modelos.py <img src="https://img.shields.io/badge/SQLAlchemy_Models-111827?style=flat&logo=sqlalchemy&logoColor=D71F00" height="18"/>
│   │   ├── modulo.py <img src="https://img.shields.io/badge/App_Factory-111827?style=flat&logo=fastapi&logoColor=009688" height="18"/>
│   │   ├── popular.py <img src="https://img.shields.io/badge/Seed_de_Dados-111827?style=flat&logo=python&logoColor=2E8B57" height="18"/>
│   │   └── principal.py <img src="https://img.shields.io/badge/-Entrypoint-111827?style=flat&logo=python&logoColor=purple" height="18"/>
│   └── requirements.txt <img src="https://img.shields.io/badge/Dependências-111827?style=flat&logo=python&logoColor=3776AB" height="18"/>
│
├── frontend <img src="https://img.shields.io/badge/HTML5-111827?style=flat&logo=html5&logoColor=E34F26" height="18"/> <img src="https://img.shields.io/badge/-CSS-111827?style=flat-square&logo=css&logoColor=663399" height="18"/> <img src="https://img.shields.io/badge/-JavaScript-111827?style=flat&logo=javascript&logoColor=F7DF1E" height="18"/>/
│   ├── html/
│   │   └── index.html <img src="https://img.shields.io/badge/-HTML5-111827?style=flat&logo=html5&logoColor=E34F26" height="18"/>
│   ├── css/
│   │   └── style.css <img src="https://img.shields.io/badge/-CSS-111827?style=flat-square&logo=css&logoColor=663399" height="18"/>
│   └── js/
│       └── app.js <img src="https://img.shields.io/badge/-JavaScript-111827?style=flat&logo=javascript&logoColor=F7DF1E" height="18"/>
│
├── docker <img src="https://img.shields.io/badge/-Docker-111827?style=flat&logo=docker&logoColor=2496ED" height="18"/>/
│   ├── Dockerfile <img src="https://img.shields.io/badge/-Dockerfile-111827?style=flat&logo=docker&logoColor=2496ED" height="18"/>
│   └── nginx.conf <img src="https://img.shields.io/badge/-Nginx-111827?style=flat&logo=nginx&logoColor=009639" height="18"/>
│
├── img/ <img src="https://img.shields.io/badge/Assets-green?style=flat&logo=image&logoColor=white" height="18"/>
├── docker-compose.yml <img src="https://img.shields.io/badge/-Docker_Compose-111827?style=flat&logo=docker&logoColor=2496ED" height="18"/>
├── .gitignore <img src="https://img.shields.io/badge/-GitIgnore-111827?style=flat&logo=git&logoColor=F05032" height="18"/>
├── LICENSE <img src="https://img.shields.io/badge/License-MIT-FF8C00?style=flat&logo=opensource&logoColor=white" height="18"/>
└── README.md <img src="https://img.shields.io/badge/-Markdown-111827?style=flat&logo=markdown&logoColor=white" height="18"/>
</pre>

<h2 align="center">🗄️ Modelos de Dados</h2>

| Modelo | Tabela | Descrição |
|---|---|---|
| **Fase** | `fases` | Grupos, Oitavas, Quartas, Semis, Final — com peso de pontuação por fase |
| **Time** | `times` | Seleções com nome e bandeira emoji |
| **Grupo** | `grupos` | Grupos A–L da fase de grupos |
| **Jogo** | `jogos` | Partidas com times, data, local, placar e status de encerramento |
| **Participante** | `participantes` | Apostadores do bolão |
| **Aposta** | `apostas` | Palpite de placar por participante/jogo com pontuação calculada |

<h2 align="center">🌐 Endpoints da API</h2>

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/jogos` | Lista jogos — filtros `?id_fase=` e `?id_grupo=` |
| `GET` | `/api/jogos/{id}` | Detalha um jogo |
| `PUT` | `/api/jogos/{id}/resultado` | Registra placar e calcula pontos das apostas |
| `PUT` | `/api/jogos/{id}/times` | Atualiza times do jogo (fases eliminatórias) |
| `GET` | `/api/apostas` | Lista apostas — filtros `?id_participante=` e `?id_jogo=` |
| `POST` | `/api/apostas` | Cria aposta `{ id_participante, id_jogo, palpite_casa, palpite_fora }` |
| `PUT` | `/api/apostas/{id}` | Atualiza palpite (somente antes do encerramento) |
| `DELETE` | `/api/apostas/{id}` | Remove aposta |
| `GET` | `/api/placar` | Ranking geral de pontos por participante |
| `GET` | `/api/fases` | Lista fases ordenadas |
| `GET` | `/api/times` | Lista seleções ordenadas por nome |
| `GET` | `/api/grupos` | Lista grupos |
| `GET` | `/api/participantes` | Lista participantes |
| `GET` | `/saude` | Health check `{ "status": "ok" }` |

> 📖 Documentação interativa disponível em **http://localhost:8000/docs** (Swagger UI) após subir o projeto.

<h2 align="center">📂 Modularização CS (Controller & Service)<br>
<img src="https://img.shields.io/badge/-FastAPI-111827?style=flat&logo=fastapi&logoColor=009688" height="18"/>
<img src="https://img.shields.io/badge/-Controller-111827?style=flat&logo=python&logoColor=F7DF1E" height="18"/>
<img src="https://img.shields.io/badge/-Service-111827?style=flat&logo=python&logoColor=3776AB" height="18"/>
</h2>

### ![Controller](https://img.shields.io/badge/Controller-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=009688) `controller/*.py`

Camada de **entrada da API**. Define rotas e métodos HTTP com FastAPI `APIRouter`. Não contém lógica de negócio — apenas valida a requisição via Pydantic e delega ao Service. Retorna os schemas de saída.

**Arquivos neste projeto:** `controller/jogos.py` · `controller/apostas.py` · `controller/placar.py`

### ![Service](https://img.shields.io/badge/Service-Python-3776AB?style=flat-square&logo=python&logoColor=3776AB) `service/*.py`

Camada de **lógica de negócio**. Processa os dados recebidos do Controller, consulta e persiste via SQLAlchemy (com `joinedload` para evitar N+1) e aplica as regras do bolão (cálculo de pontos, validações de encerramento, integridade).

**Arquivos neste projeto:** `service/jogos.py` · `service/apostas.py` · `service/placar.py`

### ![Schemas](https://img.shields.io/badge/Schemas-Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=E92063) `esquemas.py`

Camada de **validação e serialização**. Define os modelos de entrada (`*Entrada`) e saída (`*Saída`) usando Pydantic. Garante tipagem estrita nas requisições e respostas da API, e gera automaticamente o schema do Swagger UI.

**Arquivo neste projeto:** `app/esquemas.py`

### ![Models](https://img.shields.io/badge/Models-SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=D71F00) `modelos.py`

Camada de **mapeamento objeto-relacional (ORM)**. Define as tabelas do banco de dados como classes Python com SQLAlchemy `DeclarativeBase`. Gerencia relacionamentos (`relationship`) e restrições de integridade (`UniqueConstraint`, `ForeignKey`).

**Arquivo neste projeto:** `app/modelos.py`

<h2 align="center">🖥️ Frontend<br>
<img src="https://img.shields.io/badge/HTML5-111827?style=flat&logo=html5&logoColor=E34F26" height="18"/>
<img src="https://img.shields.io/badge/-CSS3-111827?style=flat&logo=css3&logoColor=1572B6" height="18"/>
<img src="https://img.shields.io/badge/-JavaScript-111827?style=flat&logo=javascript&logoColor=F7DF1E" height="18"/>
<img src="https://img.shields.io/badge/-Nginx-111827?style=flat&logo=nginx&logoColor=009639" height="18"/>
</h2>

### ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white) `html/index.html`

Página única (SPA-like) que concentra toda a interface do bolão — listagem de jogos, formulário de apostas e ranking de participantes. Consome a API via `fetch`.

### ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) `css/style.css`

Estilos visuais da aplicação. Responsável pelo layout, cores, tipografia e responsividade da interface.

### ![JS](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) `js/app.js`

Lógica client-side. Gerencia chamadas à API REST, renderiza os dados dinamicamente no DOM e trata interações do usuário (apostas, filtros, placar).

### ![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white) `docker/nginx.conf`

Serve os arquivos estáticos do frontend via Nginx Alpine e faz proxy reverso das requisições `/api/*` para o backend FastAPI.

<h2 align="center">🏆 Sistema de Pontuação</h2>

| Resultado | Saldo |
|---|---|
| **Acertou o placar exato** (e alguém acertou) | `+ R$ valor_fase` |
| **Errou** (mas alguém acertou) | `- R$ valor_fase` |
| **Ninguém acertou** | `= R$ 0,00` (neutro) |

| Fase | Valor |
|---|---|
| Fase de Grupos | R$ 1,00 |
| 16avos / 8avos / Quartas | R$ 2,00 |
| Semifinal | R$ 5,00 |
| Final | R$ 10,00 |

> Se nenhum participante acertar o placar exato de um jogo, o jogo é neutro — ninguém ganha nem perde.

<h2 align="center">🕹️ Como Rodar</h2>

Clone o repositório:

```bash
git clone https://github.com/wqiluc/Bolao-Copa-26
```

<h3 align="center">Rodar com Docker (recomendado) <br>
<img src="https://img.shields.io/badge/-Docker-111827?style=flat-square&logo=docker&logoColor=2496ed"/>
<img src="https://img.shields.io/badge/-PostgreSQL-111827?style=flat-square&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/-Nginx-111827?style=flat-square&logo=nginx&logoColor=009639"/>
</h3>

```bash
# Sobe banco, backend e frontend de uma vez (com rebuild das imagens):
docker compose up --build

# O backend executa automaticamente na inicialização:
# python -m app.popular  →  uvicorn app.principal:app

# Frontend:
http://localhost:3000

# API (Swagger UI):
http://localhost:8000/docs
```

```bash
# Parar os containers (mantém o volume do banco):
docker compose stop

# Parar e remover containers (mantém o volume do banco):
docker compose down

# Parar, remover containers E volume (reset total do banco):
docker compose down -v
```

| Serviço | URL |
|---|---|
| **Frontend** | http://localhost:3000 |
| **API (Swagger)** | http://localhost:8000/docs |
| **PostgreSQL** | localhost:5433 |

<h2 align="center">Comandos Docker Úteis <br>
<img src="https://img.shields.io/badge/-Docker-111827?style=flat-square&logo=docker&logoColor=2496ed"/>
</h2>

```bash
# Reconstrói sem usar cache (forçar rebuild completo)
docker compose build --no-cache

# Sobe em background
docker compose up -d --build

# Logs em tempo real
docker compose logs -f

# Logs de um serviço específico
docker compose logs -f backend

# Lista containers em execução
docker compose ps

# Executa shell dentro do container do backend
docker compose exec backend bash

# Reinicia um serviço específico
docker compose restart backend

# Remove containers parados, redes e imagens não usadas
docker system prune -f

# Remove também os volumes não usados (limpeza total)
docker system prune -f --volumes
```

<h2 align="center">🔑 Versões Necessárias:</h2>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=3776AB"/>
  <img src="https://img.shields.io/badge/FastAPI-0.115.0-009688?style=for-the-badge&logo=fastapi&logoColor=009688"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0.35-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00"/>
  <img src="https://img.shields.io/badge/Pydantic-2.9.2-E92063?style=for-the-badge&logo=pydantic&logoColor=E92063"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Uvicorn-0.30.6-499848?style=for-the-badge&logo=gunicorn&logoColor=499848"/>
  <img src="https://img.shields.io/badge/Docker-Engine-2496ED?style=for-the-badge&logo=docker&logoColor=2496ED"/>
  <img src="https://img.shields.io/badge/Nginx-Alpine-009639?style=for-the-badge&logo=nginx&logoColor=009639"/>
</p>
