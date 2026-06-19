const API = '/api';

const _dadosAuth = JSON.parse(localStorage.getItem('participante_auth') || 'null');

function _inicializarAuth() 
{
  const elNome = document.getElementById('nome-usuario');

  if (elNome && _dadosAuth) 
  { 
    elNome.textContent = _dadosAuth.nome;
  }

  if (localStorage.getItem('recem_logado')) 
  {
    localStorage.removeItem('recem_logado');
    setTimeout(() => toast(`Bem-vindo de volta, ${_dadosAuth?.nome || ''}!`), 300);
  }
}

function sair() 
{
  localStorage.removeItem('participante_auth');
  localStorage.removeItem('recem_logado');
  window.location.href = '/auth/login.html';
}

_inicializarAuth();

const DATAS_FASE =
{
  grupos:  { inicio: '11/Jun', fim: '27/Jun' },
  '16avas': { inicio: '28/Jun', fim: '03/Jul' },
  '8avas':  { inicio: '04/Jul', fim: '07/Jul' },
  quartas:  { inicio: '09/Jul', fim: '12/Jul' },
  semi:     { inicio: '14/Jul', fim: '15/Jul' },
  final:    { inicio: '19/Jul', fim: null },
};

let participantes = [ ], fases = [ ], times = [ ], todosJogos = [ ], classificacoes = { };

let idJogoResultado = null, idJogoAposta = null, idJogoTimes = null;

let idApostaEditando = null;

let termoBusca = '';
let filtroData = '';
let filtroResultado = '';

async function api(caminho, metodo = 'GET', corpo = null)
{
  const opts = { method: metodo, headers: { 'Content-Type': 'application/json' } };

  if (corpo)
    {
      opts.body = JSON.stringify(corpo);
    }

  const resposta = await fetch(API + caminho, opts);

  if (!resposta.ok)
    {
    const err = await resposta.json().catch(() => ({}));
      throw new Error(err.detail || resposta.statusText);
  }

  if (resposta.status === 204)
    {
      return null;
    }

  return resposta.json();
}

function toast(msg, erro = false)
{
  const elementoToast = document.getElementById('toast');
  elementoToast.textContent = msg;
  elementoToast.className = 'toast show' + (erro ? ' error' : '');
  setTimeout(() => elementoToast.className = 'toast', 3000);
}

function mostrarAba(idAba)
{
  document.querySelectorAll('.tab').forEach(aba => aba.classList.remove('active'));
  document.querySelectorAll('nav button').forEach(botao => botao.classList.remove('active'));
  document.getElementById(idAba).classList.add('active');
  const idx = ['tab-scores','tab-matches','tab-bets'].indexOf(idAba);
  document.querySelectorAll('nav button')[idx].classList.add('active');

  if (idAba === 'tab-scores')
  {
      carregarPlacar();
  }

  if (idAba === 'tab-matches')
  {
    carregarJogos();
  }

  if (idAba === 'tab-bets')
  {
    carregarApostas();
  }
}

function abrirModal(idModal)
{
  document.getElementById(idModal).classList.remove('hidden');
}

function fecharModal(idModal)
{
  document.getElementById(idModal).classList.add('hidden');
}

async function carregarPlacar()
{
  document.getElementById('scores-loading').classList.remove('hidden');
  document.getElementById('scores-content').classList.add('hidden');

  try
  {
    const pontuacoes = await api('/placar/');
    renderizarPlacar(pontuacoes);
  }

  catch(erro)
  {
    toast('Erro ao carregar placar: ' + erro.message, true);
  }

  document.getElementById('scores-loading').classList.add('hidden');
  document.getElementById('scores-content').classList.remove('hidden');
}

async function recalcularPontuacoes()
{
  const btn = document.getElementById('btn-recalcular');

  if (btn)
  {
    btn.disabled = true; btn.textContent = '⏳ Recalculando...';
  }

  try
  {
    const resultado = await api('/jogos/recalcular_tudo', 'POST');
    toast(`${resultado.recalculados} jogos recalculados!`);
    carregarPlacar();
  }

  catch(erro)
  {
    toast('Erro ao recalcular: ' + erro.message, true);
  }

  finally
  {
    if (btn)
    {
      btn.disabled = false; btn.textContent = '🔄 Recalcular Pontuações';
    }
  }
}

function formatarReais(valor)
{
  return valor.toFixed(2).replace('.', ',');
}

function renderizarSaldo(saldo)
{
  if (Math.abs(saldo) < 0.01)
  {
    return `<span class="saldo-neutro">= R$ 0,00</span>`;
  }

  if (saldo > 0)
  {
    return `<span class="saldo-positivo">▲ R$ ${formatarReais(saldo)}</span>`;
  }

  return `<span class="saldo-negativo">▼ R$ ${formatarReais(Math.abs(saldo))} a pagar</span>`;
}

function renderizarPlacar(pontuacoes)
{
  const medalhas    = ['🥇','🥈','🥉','4️⃣'];
  const classePodio = ['rank-1','rank-2','rank-3','rank-4'];

  let podio = `<div class="podium">`;
  pontuacoes.forEach((entrada, indice) =>
  {
    podio += `
      <div class="podium-card ${classePodio[indice] || ''}">
        <div class="rank">${medalhas[indice] || indice+1}</div>
        <div class="name">${entrada.participante.nome}</div>
        <div class="pts">${renderizarSaldo(entrada.saldo_total)}</div>
        <div class="sub">✅ ${entrada.acertos_exatos} acertos exatos</div>
        <div class="saldo-breakdown">
          <span class="saldo-positivo">▲ R$ ${formatarReais(entrada.total_ganho)} a receber</span>
          <span class="saldo-negativo">▼ R$ ${formatarReais(entrada.total_devido)} a pagar</span>
        </div>
      </div>`;
  });

  podio += `</div>`;

  let resumo = `
    <div class="fin-section-title">Resumo Geral</div>
    <table class="phase-table">
      <thead><tr>
        <th>Participante</th><th>Acertos</th><th>A receber</th><th>A pagar</th><th>Saldo Total</th>
      </tr></thead><tbody>`;

  pontuacoes.forEach(entrada =>
  {
    resumo += `<tr>

      <td>${entrada.participante.nome}</td>
      <td>${entrada.acertos_exatos}</td>
      <td><span class="saldo-positivo">R$ ${formatarReais(entrada.total_ganho)}</span></td>
      <td><span class="saldo-negativo">R$ ${formatarReais(entrada.total_devido)}</span></td>
      <td>${renderizarSaldo(entrada.saldo_total)}</td>
    </tr>`;
  });

  resumo += `</tbody></table>`;

  const fasesDoPlayar = pontuacoes.length > 0 ? pontuacoes[0].por_fase : [];

  let tabelasFases = '';

  fasesDoPlayar.forEach(fp0 =>
  {
    const faseId = fp0.fase.id;
    const datas   = DATAS_FASE[fp0.fase.slug];
    const dataTxt = datas ? (datas.fim ? `${datas.inicio} – ${datas.fim}` : datas.inicio) : '';
    const temMovimento = pontuacoes.some(entrada =>
    {
      const faseParticipante = entrada.por_fase.find(faseItem => faseItem.fase.id === faseId);
      return faseParticipante && (faseParticipante.ganho > 0.005 || faseParticipante.devido > 0.005);
    });

    tabelasFases += `
      <div class="fin-section-title">
        ${fp0.fase.nome}${dataTxt ? `<span class="phase-date"> ${dataTxt}</span>` : ''}
        <span class="fin-valor-badge">R$ ${formatarReais(fp0.fase.valor)}/jogo</span>
      </div>`;

    if (!temMovimento)
    {
      tabelasFases += `<div class="empty" style="padding:0.6rem 0.8rem;font-size:0.82rem">Nenhum jogo encerrado ainda nesta fase</div>`;
    }

    else
    {
      tabelasFases += `<table class="phase-table">
        <thead><tr>
          <th>Participante</th><th>Acertos</th><th>A receber</th><th>A pagar</th><th>Saldo na fase</th>
        </tr></thead><tbody>`;

      pontuacoes.forEach(entrada =>
      {
        const faseParticipante = entrada.por_fase.find(faseItem => faseItem.fase.id === faseId) || {acertos: 0, ganho: 0, devido: 0, saldo: 0};

        tabelasFases += `<tr>

          <td>${entrada.participante.nome}</td>
          <td>${faseParticipante.acertos}</td>
          <td><span class="saldo-positivo">R$ ${formatarReais(faseParticipante.ganho || 0)}</span></td>
          <td><span class="saldo-negativo">R$ ${formatarReais(faseParticipante.devido || 0)}</span></td>
          <td>${renderizarSaldo(faseParticipante.saldo || 0)}</td>
        </tr>`;
      });

      tabelasFases += `</tbody></table>`;
    }
  });

  document.getElementById('scores-content').innerHTML = podio + resumo + tabelasFases;
}

async function carregarJogos()
{
  document.getElementById('matches-loading').classList.remove('hidden');
  document.getElementById('matches-content').classList.add('hidden');

  try
  {
    const [jogos, fasesResp, clasResp] = await Promise.all
    (
      [
        api('/jogos/'),
        fases.length ? Promise.resolve(fases) : api('/fases'),
        api('/classificacoes').catch(() => []),
      ]
  );

    todosJogos = jogos;

    if (!fases.length)
    {
      fases = fasesResp;
    }

    classificacoes = { };
    clasResp.forEach(grupo => { classificacoes[grupo.grupo] = grupo.times; });

    renderizarJogos(todosJogos);
  }

  catch(erro)
  {
    toast('Erro ao carregar os jogos: ' + erro.message, true);
  }

  document.getElementById('matches-loading').classList.add('hidden');
  document.getElementById('matches-content').classList.remove('hidden');
}

function filtrarJogos(termo)
{
  termoBusca = termo.trim().toLowerCase();
  renderizarJogos(todosJogos);
}

function filtrarPorData(val)
{
  filtroData = val;
  renderizarJogos(todosJogos);
}

function filtrarHoje()
{
  const hoje = new Date();
  const iso = hoje.getFullYear() + '-'

    + String(hoje.getMonth() + 1).padStart(2, '0') + '-'
    + String(hoje.getDate()).padStart(2, '0');

  filtroData = iso;
  document.getElementById('date-filter').value = iso;

  renderizarJogos(todosJogos);
}

function selecionarFiltroResultado(btn)
{
  filtroResultado = btn.dataset.val;
  document.querySelectorAll('#bet-result-pills .pill').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  carregarApostas();
}

function limparFiltros()
{
  filtroData = '';
  termoBusca = '';
  document.getElementById('match-search').value = '';
  document.getElementById('date-filter').value = '';
  renderizarJogos(todosJogos);
}


function formatarData(iso)
{
  const date = new Date(iso);
  return date.toLocaleDateString('pt-BR', { day:'2-digit', month:'2-digit' })
  + ' ' + date.toLocaleTimeString('pt-BR', { hour:'2-digit', minute:'2-digit' });
}

function ehHoje(iso)
{
  const date = new Date(iso), hour = new Date();
  return date.toDateString() === hour.toDateString();
}

function renderizarJogos(jogos)
{
  let filtrados = jogos;

  if (termoBusca)
  {
    filtrados = filtrados.filter(jogo =>
      (jogo.time_casa?.nome || '').toLowerCase().includes(termoBusca) 
      ||
      (jogo.time_fora?.nome || '').toLowerCase().includes(termoBusca));
  }

  if (filtroData)
  {
    filtrados = filtrados.filter(jogo => jogo.data && jogo.data.startsWith(filtroData));
  }

  const porFase = { };

  filtrados.forEach(jogo =>
  {
    const idFase = jogo.fase.id;

    if (!porFase[idFase])
    {
      porFase[idFase] = { fase: jogo.fase, porGrupo: {} };
    }

    const chaveGrupo = jogo.grupo ? jogo.grupo.nome : '_eliminatoria';

    if (!porFase[idFase].porGrupo[chaveGrupo])
    {
      porFase[idFase].porGrupo[chaveGrupo] = [];
    }

    porFase[idFase].porGrupo[chaveGrupo].push(jogo);

  });

  let html = '';

  Object.values(porFase).sort((faseA, faseB) => faseA.fase.ordem - faseB.fase.ordem).forEach(({ fase, porGrupo }) =>
  {
    const jogosFlat = Object.values(porGrupo).flat();
    const total  = jogosFlat.length;
    const feitos = jogosFlat.filter(jogo => jogo.encerrado).length;
    const datas  = DATAS_FASE[fase.slug];
    const dataTxt = datas
      ? (datas.fim ? `${datas.inicio} – ${datas.fim}` : datas.inicio)
      : '';

    html += `
      <div class="phase-section">
        <div class="phase-header" onclick="alternarSecao('fase-${fase.id}')">
          <span>${fase.nome}${dataTxt ? ` <span class="phase-date">${dataTxt}</span>` : ''}</span>
          <span style="font-size:0.8rem;color:#8aabcc">${feitos}/${total} encerrados ▾</span>
        </div>
        <div id="fase-${fase.id}">`;

    Object.entries(porGrupo).sort(([chaveA], [chaveB]) => chaveA.localeCompare(chaveB)).forEach(([chaveGrupo, jogosGrupo]) =>
    {

      if (chaveGrupo !== '_eliminatoria')
      {
        html += `<div class="group-label">Grupo ${chaveGrupo}</div>`;
        const clas = classificacoes[chaveGrupo] || [];
        html += renderizarClassificacao(chaveGrupo, clas);
      }

      jogosGrupo.forEach(jogo => { html += renderizarCartaoJogo(jogo); });

    });
    html += `</div></div>`;
  });

  document.getElementById('matches-content').innerHTML =
    html || `<div class="empty">Nenhum jogo encontrado${termoBusca ? ` para "${termoBusca}"` : ''}</div>`;
}

function renderizarClassificacao(_nomeGrupo, times)
{
  if (!times || times.length === 0)
  {
    return '<div class="empty" style="padding:0.35rem 0.6rem;font-size:0.78rem;margin-bottom:0.4rem">Classificação disponível após início dos jogos</div>';
  }

  let html = '<table class="standings-table"><thead><tr>'
    + '<th>#</th><th>Time</th><th>PJ</th><th>V</th><th>E</th><th>D</th><th>GP</th><th>GC</th><th>SG</th><th>Pts</th><th></th>'
    + '</tr></thead><tbody>';

  times.forEach((time, indice) =>
  {
    const saldoGols = time.gp - time.gc;
    const sgTxt = saldoGols > 0 ? '+' + saldoGols : '' + saldoGols;
    let statusCls = '', statusTxt = '';

    if (time.pj === 0)
    {
      statusCls = '';
      statusTxt = '-';
    }

    else if (indice === 0 || indice === 1)
    {
        statusCls = 'passa-direto'; statusTxt = 'PASS';
    }

    else if (indice === 2)
    {
        statusCls = 'terceiro'; statusTxt = '?';
    }

    else
    {
      statusCls = 'eliminado'; statusTxt = 'X';
    }

    const rowCls = time.pj === 0 ? 'sem-jogos' : '';
    const sgCls  = saldoGols > 0 ? 'sg-pos' : saldoGols < 0 ? 'sg-neg' : '';

    html += '<tr class="' + rowCls + '">'
      + '<td class="pos">' + (indice + 1) + '</td>'
      + '<td class="time-nome">' + time.bandeira + ' ' + time.nome + '</td>'
      + '<td>' + time.pj + '</td><td>' + time.v + '</td><td>' + time.e + '</td><td>' + time.d + '</td>'
      + '<td>' + time.gp + '</td><td>' + time.gc + '</td>'
      + '<td class="' + sgCls + '">' + sgTxt + '</td>'
      + '<td class="pts-col">' + time.pts + '</td>'
      + '<td class="status-col ' + statusCls + '">' + statusTxt + '</td>'
      + '</tr>';
});
  html += '</tbody></table>'
    + '<div class="standings-legend">V=3pts | E=1pt | D=0 | PASS=Classificado | ?=3o aguarda | X=Eliminado</div>';

  return html;
}

function alternarSecao(idSecao)
{
  const elemento = document.getElementById(idSecao);
  elemento.style.display = elemento.style.display === 'none' ? '' : 'none';
}

function labelTime(time)
{
  if (time)
  {
    return `${time.bandeira || ''} ${time.nome}`;
  }

  return 'A definir';
}

function renderizarCartaoJogo(jogo)
{
  const classeHoje = ehHoje(jogo.data) ? 'today' : '';
  const classeEnc  = jogo.encerrado ? 'finished' : '';
  const placarHtml = jogo.encerrado
    ? `<span class="score-box">${jogo.gols_casa} – ${jogo.gols_fora}</span>`
    : `<span class="score-box pending">vs</span>`;

  let acoes = '';
  if (!jogo.encerrado)
  {

    if (!jogo.time_casa)
    {
      acoes += `<button class="btn btn-blue btn-sm" onclick="abrirModalTimes(${jogo.id})">🔗 Times</button>`;
    }

    acoes += `<button class="btn btn-gold btn-sm" onclick="abrirModalAposta(${jogo.id})">🎯 Apostar R$${jogo.fase.valor}</button>`;

    acoes += `<button class="btn btn-green btn-sm" onclick="abrirModalResultado(${jogo.id})">✅ Resultado</button>`;
  }

  const localHtml = jogo.local ? `<span class="match-local">${jogo.local}</span>` : '';

  return `
    <div class="match-card ${classeEnc} ${classeHoje}" data-id="${jogo.id}">
      <span class="match-num">#${jogo.numero}</span>
      <span class="match-date">${formatarData(jogo.data)}</span>
      ${localHtml}
      <div class="match-teams">
        <span class="team-name">${labelTime(jogo.time_casa)}</span>
        ${placarHtml}
        <span class="team-name">${labelTime(jogo.time_fora)}</span>
      </div>
      <div class="match-actions">${acoes}</div>
    </div>`;
}


function abrirModalResultado(idJogo)
{
  const jogo = todosJogos.find(jogoItem => jogoItem.id === idJogo);

  if (!jogo)
  {
    return;
  }

  idJogoResultado = idJogo;

  document.getElementById('result-modal-title').textContent = `Resultado: ${labelTime(jogo.time_casa)} x ${labelTime(jogo.time_fora)}`;
  document.getElementById('result-home-label').textContent = labelTime(jogo.time_casa);
  document.getElementById('result-away-label').textContent = labelTime(jogo.time_fora);
  document.getElementById('result-home').value = jogo.gols_casa ?? 0;
  document.getElementById('result-away').value = jogo.gols_fora ?? 0;

  abrirModal('result-modal');
}

async function buscarResultadoExterno()
{
  const btn = document.getElementById('btn-buscar-resultado');

  if (btn)
  {
    btn.disabled = true; btn.textContent = '⏳ Buscando...';
  }

  try
  {
    const resultado = await api(`/jogos/${idJogoResultado}/buscar_resultado`);
    document.getElementById('result-home').value = resultado.gols_casa;
    document.getElementById('result-away').value = resultado.gols_fora;
    toast('Placar carregado! Confirme antes de salvar.✅');
  }

  catch(erro)
  {
    toast(`Resultado ainda não disponível: ${erro.message}`, true);
  }

  finally
  {

    if (btn)
    {
      btn.disabled = false; 
      btn.textContent = '🌐 Buscar';
    }

  }
}

async function enviarResultado()
{
  try
  {
    await api(`/jogos/${idJogoResultado}/resultado`, 'PUT',
    {
      gols_casa: parseInt(document.getElementById('result-home').value),
      gols_fora: parseInt(document.getElementById('result-away').value),
    });

    toast('Resultado salvo!');
    fecharModal('result-modal');
    carregarJogos();
    carregarPlacar();
  }

  catch(erro)
  {
    toast('Erro: ' + erro.message, true);
  }
}

async function abrirModalAposta(idJogo)
{
  const jogo = todosJogos.find(jogoItem => jogoItem.id === idJogo);

  if (!jogo)
  {
    return;
  }

  idJogoAposta = idJogo;
  idApostaEditando = null;

  if (!participantes.length)
  {
    participantes = await api('/participantes');
  }

  const sel = document.getElementById('bet-modal-participant');

  sel.innerHTML = participantes.map(participante => `<option value="${participante.id}">${participante.nome}</option>`).join('');
  document.getElementById('bet-modal-title').textContent = `Apostar: ${labelTime(jogo.time_casa)} x ${labelTime(jogo.time_fora)}`;
  document.getElementById('bet-home-label').textContent = labelTime(jogo.time_casa);
  document.getElementById('bet-away-label').textContent = labelTime(jogo.time_fora);
  document.getElementById('bet-home').value = 1;
  document.getElementById('bet-away').value = 0;
  abrirModal('bet-modal');
}

async function enviarAposta()
{
  try
  {
    const idParticipante = parseInt(document.getElementById('bet-modal-participant').value);

    const casa = parseInt(document.getElementById('bet-home').value);
    const fora = parseInt(document.getElementById('bet-away').value);

    if (idApostaEditando)
    {
      await api(`/apostas/${idApostaEditando}`, 'PUT', { palpite_casa: casa, palpite_fora: fora });

      toast('Aposta atualizada! 🎰');
    }

    else
    {
      await api('/apostas/', 'POST',
      {
        id_participante: idParticipante,
        id_jogo: idJogoAposta,
        palpite_casa: casa,
        palpite_fora: fora,
      });

      toast('Aposta registrada! 🎰');
    }

    fecharModal('bet-modal');

    if (document.getElementById('tab-bets').classList.contains('active'))
    {
      carregarApostas();
    }
  }

  catch(erro)
  {
    toast('Erro: ' + erro.message, true);
  }
}

async function abrirModalTimes(idJogo)
{
  idJogoTimes = idJogo;

  if (!times.length)
  {
    times = await api('/times');
  }

  const opcoes = times.map(time => `<option value="${time.id}">${time.bandeira || ''} ${time.nome}</option>`).join('');

  document.getElementById('times-casa').innerHTML = opcoes;
  document.getElementById('times-fora').innerHTML = opcoes;

  abrirModal('teams-modal');
}

async function enviarTimes()
{
  try
  {
    await api(`/jogos/${idJogoTimes}/times`, 'PUT',
    {
      id_time_casa: parseInt(document.getElementById('times-casa').value),
      id_time_fora: parseInt(document.getElementById('times-fora').value),
    });

    toast('Times definidos!');
    fecharModal('teams-modal');
    carregarJogos();
  }

  catch(erro)
  {
    toast('Erro: ' + erro.message, true);
  }
}


async function carregarApostas()
{
  document.getElementById('bets-loading').classList.remove('hidden');
  document.getElementById('bets-content').classList.add('hidden');

  try
  {
    if (!participantes.length)
    {
      participantes = await api('/participantes');
    }

    if (!fases.length)
    {
      fases = await api('/fases');
    }

    const filtroPart = document.getElementById('bet-participant-filter');
    const filtroFase = document.getElementById('bet-phase-filter');

    if (filtroPart.options.length <= 1)
    {
      participantes.forEach(participante => filtroPart.add(new Option(participante.nome, participante.id)));
    }

    if (filtroFase.options.length <= 1)
    {
      fases.forEach(fase => filtroFase.add(new Option(fase.nome, fase.id)));
    }

    const idParticipante = filtroPart.value;
    const idFase = filtroFase.value;

    let url = '/apostas/?';

    if (idParticipante)
    {
        url += `id_participante=${idParticipante}&`;
    }

    let apostas = await api(url);

    if (idFase)
    {
      apostas = apostas.filter(aposta => aposta.jogo.fase.id === parseInt(idFase));
    }

    if (filtroResultado)
    {
      apostas = apostas.filter(aposta =>
      {
        if (filtroResultado === 'aberto') return !aposta.jogo.encerrado;
        if (!aposta.jogo.encerrado) return false;
        const pts = parseFloat(aposta.pontos);
        if (filtroResultado === 'acerto') return pts > 0.01;
        if (filtroResultado === 'errado') return pts < -0.01;
        if (filtroResultado === 'neutro') return Math.abs(pts) < 0.01;
        return true;
      });
    }

    renderizarApostas(apostas);
  }

  catch(erro)
  {
    toast('Erro ao carregar apostas: ' + erro.message, true);
  }

  document.getElementById('bets-loading').classList.add('hidden');
  document.getElementById('bets-content').classList.remove('hidden');
}

function labelPontos(aposta)
{
  if (!aposta.jogo.encerrado)
  {
    return `<span class="pts open">—</span>`;
  }

  const pontos = parseFloat(aposta.pontos);

  if (Math.abs(pontos) < 0.01)
  {
    return `<span class="pts neutro">= R$ 0,00</span>`;
  }

  if (pontos > 0)
  {
    return `<span class="pts exact">+R$ ${formatarReais(pontos)} 🎯</span>`;
  }

  return `<span class="pts wrong">-R$ ${formatarReais(Math.abs(pontos))} ✗</span>`;
}

function renderizarApostas(apostas)
{
  if (!apostas.length)
  {
    document.getElementById('bets-content').innerHTML = '<div class="empty">Nenhuma aposta encontrada</div>';
    return;
  }

  const porFase = { };
  apostas.forEach(aposta =>
  {
    const idFase = aposta.jogo.fase.id;
    if (!porFase[idFase]) porFase[idFase] =
    {
      fase: aposta.jogo.fase, apostas: []
    };

    porFase[idFase].apostas.push(aposta);

  });

  let html = '';

  Object.values(porFase).sort((faseA, faseB) => faseA.fase.ordem - faseB.fase.ordem).forEach(({ fase, apostas: apostasFase }) =>
  {
    html += `<div class="phase-header" style="margin-top:1rem">${fase.nome}</div>`;
    apostasFase.sort((apostaA, apostaB) => new Date(apostaA.jogo.data) - new Date(apostaB.jogo.data)).forEach(aposta =>
    {
      const casa = labelTime(aposta.jogo.time_casa);
      const fora = labelTime(aposta.jogo.time_fora);
      const placarStr = aposta.jogo.encerrado
        ? ` (${aposta.jogo.gols_casa}–${aposta.jogo.gols_fora})`
        : '';

      html += `

        <div class="bet-row">
          <span class="teams">${casa} x ${fora}${placarStr}</span>
          <span style="color:#8aabcc;font-size:0.8rem">${aposta.participante.nome}</span>
          <span class="pred">${aposta.palpite_casa}–${aposta.palpite_fora}</span>
          ${labelPontos(aposta)}
          ${!aposta.jogo.encerrado ? `
            <button class="btn btn-blue btn-sm" onclick="editarAposta(${aposta.id}, ${aposta.jogo.id}, '${casa}', '${fora}', ${aposta.palpite_casa}, ${aposta.palpite_fora}, ${aposta.participante.id})">✏️</button>
            <button class="btn btn-red btn-sm" onclick="deletarAposta(${aposta.id})">🗑</button>
          ` : ''}
        </div>`;
    });
  });

  document.getElementById('bets-content').innerHTML = html;
}

async function editarAposta(idAposta, idJogo, labelCasa, labelFora, palpiteCasa, palpiteFora, idParticipante)
{
  idJogoAposta = idJogo;
  idApostaEditando = idAposta;

  if (!participantes.length)
  {
    participantes = await api('/participantes');
  }

  const sel = document.getElementById('bet-modal-participant');

  sel.innerHTML = participantes.map(participante => `<option value="${participante.id}" ${participante.id==idParticipante?'selected':''}>${participante.nome}</option>`).join('');
  sel.disabled = true;
  document.getElementById('bet-modal-title').textContent = `Editar Aposta: ${labelCasa} x ${labelFora}`;
  document.getElementById('bet-home-label').textContent = labelCasa;
  document.getElementById('bet-away-label').textContent = labelFora;
  document.getElementById('bet-home').value = palpiteCasa;
  document.getElementById('bet-away').value = palpiteFora;
  abrirModal('bet-modal');
}

document.getElementById('bet-modal').addEventListener('click', evento =>
{
  if (evento.target === document.getElementById('bet-modal'))
  {
    document.getElementById('bet-modal-participant').disabled = false;
  }

});

async function deletarAposta(idAposta)
{

  if (!confirm('Remover aposta?'))
    {
      return;
    }

  try
  {
    await api(`/apostas/${idAposta}`, 'DELETE');
    toast('Aposta removida ❌');
    carregarApostas();
  }

  catch(erro)
  {
    toast('Erro: ' + erro.message, true);
  }
}

carregarPlacar();