const API = 'http://localhost:8000/api';

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

async function api(caminho, metodo = 'GET', corpo = null) 
{
  const opts = { method: metodo, headers: { 'Content-Type': 'application/json' } };

  if (corpo)
    {
      opts.body = JSON.stringify(corpo);
    }

  const r = await fetch(API + caminho, opts);

  if (!r.ok) 
    {
    const err = await r.json().catch(() => ({}));
      throw new Error(err.detail || r.statusText);
  }

  if (r.status === 204) 
    {
      return null;
    }

  return r.json();
}

function toast(msg, erro = false) 
{
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'toast show' + (erro ? ' error' : '');
  setTimeout(() => el.className = 'toast', 3000);
}

function mostrarAba(id) 
{
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  const idx = ['tab-scores','tab-matches','tab-bets'].indexOf(id);
  document.querySelectorAll('nav button')[idx].classList.add('active');

  if (id === 'tab-scores') 
  {
      carregarPlacar();
  }

  if (id === 'tab-matches') 
  {
    carregarJogos();
  }

  if (id === 'tab-bets') 
  {
    carregarApostas();
  }
}

function abrirModal(id)  
{ 
  document.getElementById(id).classList.remove('hidden'); 
}

function fecharModal(id) 
{ 
  document.getElementById(id).classList.add('hidden'); 
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

  catch(e)
  {
    toast('Erro ao carregar placar: ' + e.message, true);
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
    const r = await api('/jogos/recalcular_tudo', 'POST');
    toast(`${r.recalculados} jogos recalculados!`);
    carregarPlacar();
  }

  catch(e) 
  { 
    toast('Erro ao recalcular: ' + e.message, true); 
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
  pontuacoes.forEach((entrada, i) =>
  {
    podio += `
      <div class="podium-card ${classePodio[i] || ''}">
        <div class="rank">${medalhas[i] || i+1}</div>
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

  pontuacoes.forEach(e => 
  {
    resumo += `<tr>

      <td>${e.participante.nome}</td>
      <td>${e.acertos_exatos}</td>
      <td><span class="saldo-positivo">R$ ${formatarReais(e.total_ganho)}</span></td>
      <td><span class="saldo-negativo">R$ ${formatarReais(e.total_devido)}</span></td>
      <td>${renderizarSaldo(e.saldo_total)}</td>
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
    const temMovimento = pontuacoes.some(e => 
    {
      const fp = e.por_fase.find(f => f.fase.id === faseId);
      return fp && (fp.ganho > 0.005 || fp.devido > 0.005);
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

      pontuacoes.forEach(e => 
      {
        const fp = e.por_fase.find(f => f.fase.id === faseId) || {acertos: 0, ganho: 0, devido: 0, saldo: 0};

        tabelasFases += `<tr>

          <td>${e.participante.nome}</td>
          <td>${fp.acertos}</td>
          <td><span class="saldo-positivo">R$ ${formatarReais(fp.ganho || 0)}</span></td>
          <td><span class="saldo-negativo">R$ ${formatarReais(fp.devido || 0)}</span></td>
          <td>${renderizarSaldo(fp.saldo || 0)}</td>
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
    clasResp.forEach(g => { classificacoes[g.grupo] = g.times; });

    renderizarJogos(todosJogos);
  }

  catch(e)
  {
    toast('Erro ao carregar os jogos: ' + e.message, true);
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
      (jogo.time_casa?.nome || '').toLowerCase().includes(termoBusca) ||
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

  Object.values(porFase).sort((a, b) => a.fase.ordem - b.fase.ordem).forEach(({ fase, porGrupo }) => 
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

    Object.entries(porGrupo).sort(([a], [b]) => a.localeCompare(b)).forEach(([chaveGrupo, jogosGrupo]) =>
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

function renderizarClassificacao(nomeGrupo, times)
{
  if (!times || times.length === 0) 
  {
    return '<div class="empty" style="padding:0.35rem 0.6rem;font-size:0.78rem;margin-bottom:0.4rem">Classificação disponível após início dos jogos</div>';
  }

  let html = '<table class="standings-table"><thead><tr>'
    + '<th>#</th><th>Time</th><th>PJ</th><th>V</th><th>E</th><th>D</th><th>GP</th><th>GC</th><th>SG</th><th>Pts</th><th></th>'
    + '</tr></thead><tbody>';

  times.forEach((time, i) => 
  {
    const sg = time.gp - time.gc;
    const sgTxt = sg > 0 ? '+' + sg : '' + sg;
    let statusCls = '', statusTxt = '';

    if (time.pj === 0)
    { 
      statusCls = ''; 
      statusTxt = '-'; 
    }

    else if (i === 0 || i === 1) 
    { 
        statusCls = 'passa-direto'; statusTxt = 'PASS'; 
    }

    else if (i === 2) 
    { 
        statusCls = 'terceiro'; statusTxt = '?'; 
    }

    else 
    { 
      statusCls = 'eliminado'; statusTxt = 'X'; 
    }

    const rowCls = time.pj === 0 ? 'sem-jogos' : '';
    const sgCls  = sg > 0 ? 'sg-pos' : sg < 0 ? 'sg-neg' : '';

    html += '<tr class="' + rowCls + '">'
      + '<td class="pos">' + (i + 1) + '</td>'
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

function alternarSecao(id)
{
  const el = document.getElementById(id);
  el.style.display = el.style.display === 'none' ? '' : 'none';
}

function labelTime(time) 
{
  if (time) 
  {
    return `${time.bandeira || ''} ${time.nome}`;
  }

  return 'A definir';
}

function renderizarCartaoJogo(j) 
{
  const classeHoje = ehHoje(j.data) ? 'today' : '';
  const classeEnc  = j.encerrado ? 'finished' : '';
  const placarHtml = j.encerrado
    ? `<span class="score-box">${j.gols_casa} – ${j.gols_fora}</span>`
    : `<span class="score-box pending">vs</span>`;

  let acoes = '';
  if (!j.encerrado)
  {
    
    if (!j.time_casa) 
    {
      acoes += `<button class="btn btn-blue btn-sm" onclick="abrirModalTimes(${j.id})">🔗 Times</button>`;
    }

    acoes += `<button class="btn btn-gold btn-sm" onclick="abrirModalAposta(${j.id})">🎯 Apostar R$${j.fase.valor}</button>`;

    acoes += `<button class="btn btn-green btn-sm" onclick="abrirModalResultado(${j.id})">✅ Resultado</button>`;
  }

  const localHtml = j.local ? `<span class="match-local">${j.local}</span>` : '';

  return `
    <div class="match-card ${classeEnc} ${classeHoje}" data-id="${j.id}">
      <span class="match-num">#${j.numero}</span>
      <span class="match-date">${formatarData(j.data)}</span>
      ${localHtml}
      <div class="match-teams">
        <span class="team-name">${labelTime(j.time_casa)}</span>
        ${placarHtml}
        <span class="team-name">${labelTime(j.time_fora)}</span>
      </div>
      <div class="match-actions">${acoes}</div>
    </div>`;
}


function abrirModalResultado(idJogo) 
{
  const j = todosJogos.find(x => x.id === idJogo);

  if (!j)
  {
    return;
  }

  idJogoResultado = idJogo;

  document.getElementById('result-modal-title').textContent = `Resultado: ${labelTime(j.time_casa)} x ${labelTime(j.time_fora)}`;
  document.getElementById('result-home-label').textContent = labelTime(j.time_casa);
  document.getElementById('result-away-label').textContent = labelTime(j.time_fora);
  document.getElementById('result-home').value = j.gols_casa ?? 0;
  document.getElementById('result-away').value = j.gols_fora ?? 0;

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
    const r = await api(`/jogos/${idJogoResultado}/buscar_resultado`);
    document.getElementById('result-home').value = r.gols_casa;
    document.getElementById('result-away').value = r.gols_fora;
    toast('Placar carregado da API! Confirme antes de salvar.');
  }

  catch(e)
  {
    toast('Resultado ainda não disponível: ' + e.message, true);
  }

  finally
  {

    if (btn) 
    { 
      btn.disabled = false; btn.textContent = '🌐 Buscar'; 
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

  catch(e)
  {
    toast('Erro: ' + e.message, true);
  }
}

async function abrirModalAposta(idJogo)
{
  const j = todosJogos.find(x => x.id === idJogo);

  if (!j)
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

  sel.innerHTML = participantes.map(p => `<option value="${p.id}">${p.nome}</option>`).join('');
  document.getElementById('bet-modal-title').textContent = `Apostar: ${labelTime(j.time_casa)} x ${labelTime(j.time_fora)}`;
  document.getElementById('bet-home-label').textContent = labelTime(j.time_casa);
  document.getElementById('bet-away-label').textContent = labelTime(j.time_fora);
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

      toast('Aposta registrada!');
    }

    fecharModal('bet-modal');

    if (document.getElementById('tab-bets').classList.contains('active')) 
    { 
      carregarApostas();
    }
  } 

  catch(e) 
  { 
    toast('Erro: ' + e.message, true); 
  }
}

async function abrirModalTimes(idJogo) 
{
  idJogoTimes = idJogo;

  if (!times.length)
  {
    times = await api('/times');
  }

  const opcoes = times.map(t => `<option value="${t.id}">${t.bandeira || ''} ${t.nome}</option>`).join('');

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
  
  catch(e) 
  { 
    toast('Erro: ' + e.message, true); 
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

    renderizarApostas(apostas);
  } 

  catch(e) 
  { 
    toast('Erro ao carregar apostas: ' + e.message, true); 
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

  Object.values(porFase).sort((a, b) => a.fase.ordem - b.fase.ordem).forEach(({ fase, apostas: apostasFase }) => 
  {
    html += `<div class="phase-header" style="margin-top:1rem">${fase.nome}</div>`;
    apostasFase.sort((a, b) => new Date(a.jogo.data) - new Date(b.jogo.data)).forEach(aposta => 
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

  sel.innerHTML = participantes.map(p => `<option value="${p.id}" ${p.id==idParticipante?'selected':''}>${p.nome}</option>`).join('');
  sel.disabled = true;
  document.getElementById('bet-modal-title').textContent = `Editar Aposta: ${labelCasa} x ${labelFora}`;
  document.getElementById('bet-home-label').textContent = labelCasa;
  document.getElementById('bet-away-label').textContent = labelFora;
  document.getElementById('bet-home').value = palpiteCasa;
  document.getElementById('bet-away').value = palpiteFora;
  abrirModal('bet-modal');
}

document.getElementById('bet-modal').addEventListener('click', e => 
{
  if (e.target === document.getElementById('bet-modal')) 
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

  catch(e) 
  { 
    toast('Erro: ' + e.message, true); 
  }
}

carregarPlacar();