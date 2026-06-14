<h1 align="center"> Bolão Copa do Mundo 2026 🏆⚽🌎 <br>
<img src="./img/logofifa.jpeg" width="420" alt="Logo FIFA 2026"/></h1>

<h2 align="center">💻⛏️ Tecnologias e Ferramentas Utilizadas: <br>
<img src="https://img.shields.io/badge/Tech_Stack-111827?style=flat-square&logo=stackshare&logoColor=whitesmoke"/></h2>
<p align="center">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/vscode/vscode-original.svg" height="25" alt="VS Code"/> <br>
  <img src="https://img.shields.io/badge/FIFA-111827?style=for-the-badge&logo=fifa&logoColor=yellow" height="25" alt="FIFA"/>
  <img src="https://img.shields.io/badge/Architecture-111827?style=flat-square&logo=instructure&logoColor=white" height="25" alt="Arquitetura"/>
  <img src="https://img.shields.io/badge/Python-111827?style=for-the-badge&logo=python&logoColor=3776AB" height="25" alt="Python"/>
  <img src="https://img.shields.io/badge/PyAutoGUI-111827?style=for-the-badge&logo=python&logoColor=yellow" height="25" alt="PyAutoGUI"/>
  <img src="https://img.shields.io/badge/os_(macOS)-111827?style=for-the-badge&logo=apple&logoColor=white" height="25" alt="os macOS"/> <br>
  <img src="https://img.shields.io/badge/FastAPI-111827?style=for-the-badge&logo=fastapi&logoColor=009688" height="25" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-111827?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00" height="25" alt="SQLAlchemy"/>
  <img src="https://img.shields.io/badge/Pydantic-111827?style=for-the-badge&logo=pydantic&logoColor=E92063" height="25" alt="Pydantic"/>
  <img src="https://img.shields.io/badge/PostgreSQL-111827?style=for-the-badge&logo=postgresql&logoColor=white" height="25" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Docker-111827?style=for-the-badge&logo=docker&logoColor=2496ED" height="25" alt="Docker"/>
  <img src="https://img.shields.io/badge/Nginx-111827?style=for-the-badge&logo=nginx&logoColor=009639" height="25" alt="Nginx"/> <br>
  <img src="https://img.shields.io/badge/HTML5-111827?style=for-the-badge&logo=html5&logoColor=E34F26" height="25" alt="HTML5"/>
  <img src="https://img.shields.io/badge/-CSS3-111827?style=flat-square&logo=css&logoColor=663399" height="25" alt="CSS3"/>
  <img src="https://img.shields.io/badge/JavaScript-111827?style=for-the-badge&logo=javascript&logoColor=F7DF1E" height="25" alt="JavaScript"/>
  <img src="https://img.shields.io/badge/-Swagger-111827?style=flat-square&logo=swagger&logoColor=85EA2D" height="25" alt="Swagger"/>
  <img src="https://img.shields.io/badge/openapi.yml-111827?style=flat-square&logo=openapiinitiative&logoColor=green" height="25" alt="OpenApi"/> <br>
  <img src="https://img.shields.io/badge/Git-111827?style=for-the-badge&logo=git&logoColor=F05032" height="25" alt="Git"/>
  <img src="https://img.shields.io/badge/GitHub-111827?style=for-the-badge&logo=github&logoColor=white" height="25" alt="GitHub"/>
  <img src="https://img.shields.io/badge/GitHub_Desktop-111827?style=for-the-badge&logo=github&logoColor=purple" height="25" alt="GitHub Desktop"/>
</p>

<h2 align="center">🏰 Arquitetura do Projeto <br>
<img src="https://img.shields.io/badge/Architecture-111827?style=flat-square&logo=instructure&logoColor=white"/></h2>

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
│   │   │   ├── placar.py <img src="https://img.shields.io/badge/Service_Placar-111827?style=flat&logo=python&logoColor=3776AB" height="18"/>
│   │   │   └── resultado_externo.py <img src="https://img.shields.io/badge/Fonte_Externa-111827?style=flat&logo=python&logoColor=F7DF1E" height="18"/>
│   │   ├── color <img src="https://img.shields.io/badge/Terminal_Colors-111827?style=flat&logo=gnometerminal&logoColor=white" height="18"/>/
│   │   │   └── cores.py <img src="https://img.shields.io/badge/ANSI_Colors-111827?style=flat&logo=python&logoColor=3776AB" height="18"/>
│   │   ├── banco.py <img src="https://img.shields.io/badge/Conexão_BD-111827?style=flat&logo=postgresql&logoColor=white" height="18"/>
│   │   ├── esquemas.py <img src="https://img.shields.io/badge/Pydantic_Schemas-111827?style=flat&logo=pydantic&logoColor=E92063" height="18"/>
│   │   ├── modelos.py <img src="https://img.shields.io/badge/SQLAlchemy_Models-111827?style=flat&logo=sqlalchemy&logoColor=D71F00" height="18"/>
│   │   ├── modulo.py <img src="https://img.shields.io/badge/App_Factory-111827?style=flat&logo=fastapi&logoColor=009688" height="18"/>
│   │   ├── popular.py <img src="https://img.shields.io/badge/Seed_de_Dados-111827?style=flat&logo=python&logoColor=2E8B57" height="18"/>
│   │   ├── principal.py <img src="https://img.shields.io/badge/-Entrypoint-111827?style=flat&logo=python&logoColor=purple" height="18"/>
│   │   ├── apoio.py <img src="https://img.shields.io/badge/Dev_Helper-111827?style=flat&logo=python&logoColor=F7DF1E" height="18"/>
│   │   └── pesquisar_jogo.py <img src="https://img.shields.io/badge/Automação_GUI-111827?style=flat&logo=python&logoColor=009688" height="18"/>
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
│   ├── docker-compose.yml <img src="https://img.shields.io/badge/-Docker_Compose-111827?style=flat&logo=docker&logoColor=2496ED" height="18"/>
│   ├── Dockerfile <img src="https://img.shields.io/badge/-Dockerfile-111827?style=flat&logo=docker&logoColor=2496ED" height="18"/>
│   ├── nginx.conf <img src="https://img.shields.io/badge/-Nginx-111827?style=flat&logo=nginx&logoColor=009639" height="18"/>
│
├── api <img src="https://img.shields.io/badge/OpenAPI-111827?style=flat&logo=openapiinitiative&logoColor=green" height="18"/>/
│   └── openapi.yml <img src="https://img.shields.io/badge/OpenAPI_3.1-Spec-6BA539?style=flat&logo=openapiinitiative&logoColor=white" height="18"/>
│
├── img/ <img src="https://img.shields.io/badge/Assets-green?style=flat&logo=image&logoColor=white" height="18"/>
├── .gitignore <img src="https://img.shields.io/badge/-GitIgnore-111827?style=flat&logo=git&logoColor=F05032" height="18"/>
├── LICENSE <img src="https://img.shields.io/badge/License-MIT-FF8C00?style=flat&logo=opensource&logoColor=white" height="18"/>
└── README.md <img src="https://img.shields.io/badge/-Markdown-111827?style=flat&logo=markdown&logoColor=white" height="18"/>
</pre>

<h2 align="center">🎲 Modelos de Dados <br>
<img src="https://img.shields.io/badge/Data_Models-111827?style=flat-square&logo=sqlalchemy&logoColor=D71F00"/></h2>

| Modelo | Tabela | Descrição |
|---|---|---|
| **Fase** | `fases` | Grupos, Oitavas, Quartas, Semis, Final — com peso de pontuação por fase |
| **Time** | `times` | Seleções com nome e bandeira emoji |
| **Grupo** | `grupos` | Grupos A–L da fase de grupos |
| **Jogo** | `jogos` | Partidas com times, data, local, placar e status de encerramento |
| **Participante** | `participantes` | Apostadores do bolão |
| **Aposta** | `apostas` | Palpite de placar por participante/jogo com pontuação calculada |

<h2 align="center">🌐 Endpoints da API (rotas) <br>
<img src="https://img.shields.io/badge/REST_API-111827?style=flat-square&logo=swagger&logoColor=cyan"/></h2>

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/jogos` | Lista jogos — filtros `?id_fase=` e `?id_grupo=` |
| `GET` | `/api/jogos/{id}` | Detalha um jogo |
| `PUT` | `/api/jogos/{id}/resultado` | Registra placar, calcula pontos e avança vencedor no chaveamento |
| `PUT` | `/api/jogos/{id}/times` | Atualiza times do jogo (fases eliminatórias) |
| `GET` | `/api/jogos/{id}/buscar_resultado` | Busca placar na fonte externa (openfootball) com cache de 5 min |
| `POST` | `/api/jogos/recalcular_tudo` | Re-aplica a pontuação em todos os jogos encerrados |
| `GET` | `/api/apostas` | Lista apostas — filtros `?id_participante=` e `?id_jogo=` |
| `POST` | `/api/apostas` | Cria aposta `{ id_participante, id_jogo, palpite_casa, palpite_fora }` |
| `PUT` | `/api/apostas/{id}` | Atualiza palpite <b>(somente antes do encerramento)</b> |
| `DELETE` | `/api/apostas/{id}` | Remove aposta |
| `GET` | `/api/placar` | Ranking com breakdown financeiro por fase (saldo, ganho, devido, acertos) |
| `GET` | `/api/classificacoes` | Classificação de todos os grupos (pontos FIFA: V=3, E=1, D=0) |
| `GET` | `/api/fases` | Lista fases ordenadas |
| `GET` | `/api/times` | Lista seleções ordenadas por nome |
| `GET` | `/api/grupos` | Lista grupos |
| `GET` | `/api/participantes` | Lista participantes |
| `GET` | `/saude` | Health check `{ "status": "ok" }` |

> 📖 Documentação interativa disponível em **http://localhost:8000/docs** (Swagger UI) <br>
> 📄 Spec completo em [`api/openapi.yml`](api/openapi.yml) — OpenAPI 3.1, gerado diretamente do FastAPI

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

**Arquivos neste projeto:** `service/jogos.py` · `service/apostas.py` · `service/placar.py` · `service/resultado_externo.py`

### ![Schemas](https://img.shields.io/badge/Schemas-Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=E92063) `esquemas.py`

Camada de **validação e serialização**. Define os modelos de entrada (`*Entrada`) e saída (`*Saída`) usando Pydantic. Garante tipagem estrita nas requisições e respostas da API, e gera automaticamente o schema do Swagger UI.

**Arquivo neste projeto:** `app/esquemas.py`

### ![Models](https://img.shields.io/badge/Models-SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=D71F00) `modelos.py`

Camada de **mapeamento objeto-relacional (ORM)**. Define as tabelas do banco de dados como classes Python com SQLAlchemy `DeclarativeBase`. Gerencia relacionamentos (`relationship`) e restrições de integridade (`UniqueConstraint`, `ForeignKey`).

**Arquivo neste projeto:** `app/modelos.py`

### ![Python](https://img.shields.io/badge/resultado__externo.py-111827?style=flat-square&logo=python&logoColor=F7DF1E) `service/resultado_externo.py`

Módulo de **integração com fonte externa de resultados**. Consulta o feed público [openfootball/worldcup.json](https://github.com/openfootball/worldcup.json) para obter placares reais da Copa 2026. Implementa cache em memória com TTL de 5 minutos para evitar requisições repetidas. Usado pelo endpoint `GET /api/jogos/{id}/buscar_resultado` e pelo botão **🌐 Buscar** no modal de registro de resultado do frontend.

<h2 align="center">🛠️ Scripts Utilitários (Automação GUI)<br>
<img src="https://img.shields.io/badge/PyAutoGUI-111827?style=flat&logo=python&logoColor=F7DF1E" height="18"/>
<img src="https://img.shields.io/badge/Terminal_Colors-111827?style=flat&logo=gnometerminal&logoColor=white" height="18"/>
</h2>

Scripts independentes do servidor FastAPI — executados diretamente no terminal para auxiliar no desenvolvimento e uso do bolão.

### ![Python](https://img.shields.io/badge/color/cores.py-111827?style=flat-square&logo=python&logoColor=3776AB) `color/cores.py`

Módulo de **constantes de cores ANSI** para saída formatada no terminal. Define variáveis como `Verde`, `Amarelo`, `CinzaClaro`, `Reset`, etc., importadas pelos scripts de automação para colorir as mensagens impressas no console.

### ![Python](https://img.shields.io/badge/apoio.py-111827?style=flat-square&logo=python&logoColor=F7DF1E) `apoio.py`

Script de **apoio ao desenvolvimento da automação GUI**. Aguarda 7 segundos (tempo para posicionar o mouse) e imprime as coordenadas exatas do cursor via `pyautogui.position()`. Usado para descobrir as posições de tela necessárias na construção dos scripts de automação.

```py
python backend/app/apoio.py
# → posicione o mouse e aguarde → imprime (x, y)
import pyautogui
from time import (sleep)

#👇🧭: 
sleep(7)
print(pyautogui.position())
```

### ![Python](https://img.shields.io/badge/pesquisar_jogo.py-111827?style=flat-square&logo=python&logoColor=009688) `pesquisar_jogo.py`

Script de **automação GUI** que abre o Google Chrome e pesquisa automaticamente por *"Jogos da Copa na data de hoje"* no navegador, exibindo uma mensagem colorida no terminal ao concluir. Depende de `color/cores.py` para formatação e de `pyautogui` para o controle do teclado.

```py
import os
import pyautogui as auto
from time import sleep
from color.cores import *

navegador = "Google Chrome"
mensagem = "Jogos da Copa na data de hoje"

os.system(f"open -a '{navegador}'")
sleep(0.9)
auto.press("enter")

auto.write(f"{mensagem}")
sleep(0.5)
auto.press("enter")

print(f"\n{CinzaClaro}Seguem os Jogos da {Reset}{Verde}Copa do Mundo 🏆{Reset}{CinzaClaro} de Hoje{Reset} {Amarelo}no seu navegador!!{Reset}\n")
```

<h2 align="center">🖥️ Frontend<br>
<img src="https://img.shields.io/badge/HTML5-111827?style=flat&logo=html5&logoColor=E34F26" height="18"/>
<img src="https://img.shields.io/badge/-CSS-111827?style=flat-square&logo=css&logoColor=663399" height="18"/>
<img src="https://img.shields.io/badge/-JavaScript-111827?style=flat&logo=javascript&logoColor=F7DF1E" height="18"/>
<img src="https://img.shields.io/badge/-Nginx-111827?style=flat&logo=nginx&logoColor=009639" height="18"/>
</h2>

### ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=black) `html/index.html`

Página única (SPA-like) que concentra toda a interface do bolão — listagem de jogos, formulário de apostas e ranking de participantes. Consome a API via `fetch`.

Novidades de interface:
- **🔄 Recalcular Pontuações** — botão na aba de placar que chama `POST /api/jogos/recalcular_tudo` e recarrega o ranking
- **🌐 Buscar** — botão no modal de resultado que preenche automaticamente o placar via `GET /api/jogos/{id}/buscar_resultado`
- **Filtro por data** — seletor de data + botão **Hoje** + botão **✕ Limpar** na aba de jogos

### ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white) `css/style.css`

Estilos visuais da aplicação. Responsável pelo layout, cores, tipografia e responsividade da interface.

Novos estilos: `.standings-table` (tabela de classificação de grupos), `.fin-section-title` / `.fin-valor-badge` (breakdown financeiro por fase), `.match-filters` / `.date-filter-row` (filtros de data), `.pts.neutro` (jogo sem acertadores).

### ![JS](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black) `js/app.js`

Lógica client-side. Gerencia chamadas à API REST, renderiza os dados dinamicamente no DOM e trata interações do usuário (apostas, filtros, placar).

Novidades:
- `recalcularPontuacoes()` — dispara recálculo geral e recarrega o placar
- `buscarResultadoExterno()` — busca o placar real e preenche o modal automaticamente
- `filtrarPorData()` / `filtrarHoje()` / `limparFiltros()` — filtros de data na listagem de jogos
- `renderizarPlacar()` — exibe resumo geral + tabelas detalhadas por fase (acertos, ganho, a pagar, saldo)
- Carregamento das classificações de grupos via `GET /api/classificacoes`

### ![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=black) `docker/nginx.conf`

Serve os arquivos estáticos do frontend via Nginx Alpine e faz proxy reverso das requisições `/api/*` para o backend FastAPI.

<h2 align="center">🏆 Sistema de Pontuação <br>
<img src="https://img.shields.io/badge/Pontuação-111827?style=flat-square&logo=fifa&logoColor=yellow"/></h2>

| Resultado | Saldo |
|---|---|
| **Acertou o placar exato** (único) | `+ R$ valor_fase × nº de erros` (fica com o bolo inteiro) |
| **Acertou o placar exato** (múltiplos) | `+ R$ (valor_fase × nº de erros) ÷ nº de acertadores` (prêmio dividido) |
| **Errou** (mas alguém acertou) | `- R$ valor_fase` |
| **Ninguém acertou** | `= R$ 0,00` (neutro) |

| Fase | Valor |
|---|---|
| Fase de Grupos | R$ 1,00 |
| 16avos / 8avos / Quartas | R$ 2,00 |
| Semifinal | R$ 5,00 |
| Final | R$ 10,00 |

> Se nenhum participante acertar o placar exato de um jogo, o jogo é neutro — ninguém ganha nem perde.  
> Quando múltiplos participantes acertam o mesmo placar, o prêmio total (soma de todos os R$ pagos pelos perdedores) é dividido igualmente entre eles.

<h2 align="center">⚙️ Chaveamento Eliminatório <br>
<img src="https://img.shields.io/badge/Bracket-111827?style=flat-square&logo=fifa&logoColor=yellow"/></h2>

Ao registrar o resultado de um jogo eliminatório, o backend avança automaticamente o time vencedor para o próximo jogo do chaveamento. O mapeamento `CHAVE_PROXIMO_JOGO` em `service/jogos.py` codifica o bracket completo da Copa 2026:

| Rodada | Jogos | → |
|---|---|---|
| 16avos (jg 73–88) | → 8avos (jg 89–96) | slot `casa` ou `fora` do próximo jogo |
| 8avos (jg 89–96) | → Quartas (jg 97–100) | |
| Quartas (jg 97–100) | → Semis (jg 101–102) | |
| Semis (jg 101–102) | → Final (jg 103) | |

> Em caso de empate no tempo regulamentar, o slot não é preenchido automaticamente — times devem ser atribuídos manualmente via `PUT /api/jogos/{id}/times`.

<h2 align="center">🕹️ Como Rodar <br>
<img src="https://img.shields.io/badge/-🕹️%20Terminal-020617?style=flat-square" alt="Terminal"></h2>

<h3 align="center">Rodar com Docker<br>
<img src="https://img.shields.io/badge/-Docker-111827?style=flat-square&logo=docker&logoColor=2496ed"/>
<img src="https://img.shields.io/badge/-PostgreSQL-111827?style=flat-square&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/-Nginx-111827?style=flat-square&logo=nginx&logoColor=009639"/>
</h3>

```bash
# Sobe banco, backend e frontend de uma vez (com rebuild das imagens):
docker compose -f docker/docker-compose.yml up --build

# O backend executa automaticamente na inicialização:
# python -m app.popular  →  uvicorn app.principal:app

# Frontend:
http://localhost:3000

# API (Swagger UI):
http://localhost:8000/docs
```

```bash
# Parar os containers (mantém o volume do banco):
docker compose -f docker/docker-compose.yml stop

# Parar e remover containers (mantém o volume do banco):
docker compose -f docker/docker-compose.yml down

# Parar, remover containers E volume (reset total do banco):
docker compose -f docker/docker-compose.yml down -v
```

| Serviço 🔑 | URL 🔗 |
|---|---|
| **Frontend** | http://localhost:3000 |
| **API (Swagger)** | http://localhost:8000/docs |
| **PostgreSQL** | localhost:5433 |

<h2 align="center">Comandos Docker Úteis <br>
<img src="https://img.shields.io/badge/-Docker-111827?style=flat-square&logo=docker&logoColor=2496ed"/>
</h2>

```bash
# Reconstrói sem usar cache (forçar rebuild completo)
docker compose -f docker/docker-compose.yml build --no-cache

# Sobe em background
docker compose -f docker/docker-compose.yml up -d --build

# Logs em tempo real
docker compose -f docker/docker-compose.yml logs -f

# Logs de um serviço específico
docker compose -f docker/docker-compose.yml logs -f backend

# Lista containers em execução
docker compose -f docker/docker-compose.yml ps

# Executa shell dentro do container do backend
docker compose -f docker/docker-compose.yml exec backend bash

# Reinicia um serviço específico
docker compose -f docker/docker-compose.yml restart backend

# Remove containers parados, redes e imagens não usadas
docker system prune -f

# Remove também os volumes não usados (limpeza total)
docker system prune -f --volumes
```

<h2 align="center">🔑 Versões Necessárias: <br>
<img src="https://img.shields.io/badge/Requirements-111827?style=flat-square&logo=dependabot&logoColor=yellow"/></h2>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=3776AB"/>
  <img src="https://img.shields.io/badge/FastAPI-0.115.0-009688?style=for-the-badge&logo=fastapi&logoColor=009688"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0.35-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00"/>
  <img src="https://img.shields.io/badge/Pydantic-2.9.2-E92063?style=for-the-badge&logo=pydantic&logoColor=E92063"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16+-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Uvicorn-0.30.6-499848?style=for-the-badge&logo=gunicorn&logoColor=499848"/>
  <img src="https://img.shields.io/badge/Docker-Engine-2496ED?style=for-the-badge&logo=docker&logoColor=2496ED"/>
  <img src="https://img.shields.io/badge/Nginx-Alpine-009639?style=for-the-badge&logo=nginx&logoColor=009639"/>
</p>

<h2 align="center">Acompanhe os Jogos da Copa do Mundo 2026 ⚽️🏆 <br>
<img src="https://img.shields.io/badge/Copa_2026-111827?style=flat-square&logo=fifa&logoColor=yellow"/></h2>
<p align="center">
  Confira partidas passadas, próximos jogos e placares em tempo real no Globo Esporte:<br><br>
  <a href="https://ge.globo.com/futebol/copa-do-mundo/">
    <img src="https://img.shields.io/badge/Globo_Esporte-Ver_Jogos_%26_Resultados-yellow?style=for-the-badge&logo=globo&logoColor=white" height="25" alt="Globo Esporte - Jogos e Resultados"/>
  </a>
</p>
