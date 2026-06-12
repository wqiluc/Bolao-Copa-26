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

let participantes = [], fases = [], times = [], todosJogos = [];
let idJogoResultado = null, idJogoAposta = null, idJogoTimes = null;
let idApostaEditando = null;
let termoBusca = '';

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
  if (id === 'tab-scores')  carregarPlacar();
  if (id === 'tab-matches') carregarJogos();
  if (id === 'tab-bets')    carregarApostas();
}

function abrirModal(id)  { document.getElementById(id).classList.remove('hidden'); }
function fecharModal(id) { document.getElementById(id).classList.add('hidden'); }

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

function renderizarSaldo(saldo)
{
  if (Math.abs(saldo) < 0.01)
  {
    return `<span class="saldo-neutro">= R$ 0,00</span>`;
  }

  if (saldo > 0)
  {
    return `<span class="saldo-positivo">▲ R$ ${saldo.toFixed(2).replace('.',',')}</span>`;
  }

  return `<span class="saldo-negativo">▼ R$ ${Math.abs(saldo).toFixed(2).replace('.',',')} a pagar</span>`;
}

function renderizarPlacar(pontuacoes)
{
  const medalhas    = ['🥇','🥈','🥉','4️⃣'];
  const classePodio = ['rank-1','rank-2','rank-3','rank-4'];

  let podio = `<div class="podium">`;
  pontuacoes.forEach((p, i) =>
  {
    podio += `
      <div class="podium-card ${classePodio[i] || ''}">
        <div class="rank">${medalhas[i] || i+1}</div>
        <div class="name">${p.participante.nome}</div>
        <div class="pts">${renderizarSaldo(p.saldo_total)}</div>
        <div class="sub">✅ ${p.acertos_exatos} acertos exatos</div>
      </div>`;
  });
  podio += `</div>`;

  const nomesFases = pontuacoes.length > 0
    ? pontuacoes[0].por_fase.map(f => f.fase.nome)
    : [];

  let tabela = `<table class="phase-table">
    <thead><tr>
      <th>Participante</th>
      ${nomesFases.map(n => `<th>${n}</th>`).join('')}
      <th>Saldo</th>
    </tr></thead><tbody>`;

  pontuacoes.forEach((p) =>
  {
    tabela += `<tr>
      <td>${p.participante.nome}</td>
      ${p.por_fase.map(f => {
        const s = f.saldo ?? 0;
        const txt = (s > 0 ? '+' : '') + s.toFixed(2).replace('.',',');
        const cls = s > 0.005 ? 'saldo-positivo' : s < -0.005 ? 'saldo-negativo' : 'saldo-neutro';
        return `<td><span class="${cls}">R$ ${txt}</span></td>`;
      }).join('')}
      <td>${renderizarSaldo(p.saldo_total)}</td>
    </tr>`;
  });
  tabela += `</tbody></table>`;

  document.getElementById('scores-content').innerHTML = podio + tabela;
}

async function carregarJogos() 
{
  document.getElementById('matches-loading').classList.remove('hidden');
  document.getElementById('matches-content').classList.add('hidden');

  try 
  {
    todosJogos = await api('/jogos/');
    fases = fases.length ? fases : await api('/fases');
    renderizarJogos(todosJogos);
  } 

  catch(e) 
  { 
    toast('Erro ao carregar jogos: ' + e.message, true); 
  }

  document.getElementById('matches-loading').classList.add('hidden');
  document.getElementById('matches-content').classList.remove('hidden');
}

function filtrarJogos(termo) 
{
  termoBusca = termo.trim().toLowerCase();
  renderizarJogos(todosJogos);
}


function formatarData(iso) 
{
  const d = new Date(iso);
  return d.toLocaleDateString('pt-BR', { day:'2-digit', month:'2-digit' })
       + ' ' + d.toLocaleTimeString('pt-BR', { hour:'2-digit', minute:'2-digit' });
}

function ehHoje(iso) 
{
  const d = new Date(iso), h = new Date();
  return d.toDateString() === h.toDateString();
}

function renderizarJogos(jogos) 
{
  const filtrados = termoBusca
    ? jogos.filter(j => (j.time_casa?.nome || '').toLowerCase().includes(termoBusca) || 
    (j.time_fora?.nome || '').toLowerCase().includes(termoBusca))
    : jogos;

  const porFase = {};
  filtrados.forEach(j => 
  {
    const chave = j.fase.id;
    if (!porFase[chave]) 
    { 
      porFase[chave] = { fase: j.fase, porGrupo: {} };
    }

    const g = j.grupo ? j.grupo.nome : '_eliminatoria';

    if (!porFase[chave].porGrupo[g])
    {
      porFase[chave].porGrupo[g] = [];
    }

    porFase[chave].porGrupo[g].push(j);
  });

  let html = '';
  Object.values(porFase).sort((a,b) => a.fase.ordem - b.fase.ordem).forEach(({ fase, porGrupo }) => {
    const total  = Object.values(porGrupo).flat().length;
    const feitos = Object.values(porGrupo).flat().filter(j => j.encerrado).length;
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

    Object.entries(porGrupo).sort(([a],[b]) => a.localeCompare(b)).forEach(([grp, jogosGrupo]) => 
    {
      if (grp !== '_eliminatoria')
        { 
          html += `<div class="group-label">Grupo ${grp}</div>`;
        }
      jogosGrupo.forEach(j => { html += renderizarCartaoJogo(j); });
    });
    html += `</div></div>`;
  });

  document.getElementById('matches-content').innerHTML =
    html || `<div class="empty">Nenhum jogo encontrado${termoBusca ? ` para "${termoBusca}"` : ''}</div>`;
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


function abrirModalResultado(idJogo) {
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
      toast('Aposta atualizada!');
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
    if (document.getElementById('tab-bets').classList.contains('active')) carregarApostas();
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

  const opts = times.map(t => `<option value="${t.id}">${t.bandeira || ''} ${t.nome}</option>`).join('');
  document.getElementById('times-casa').innerHTML = opts;
  document.getElementById('times-fora').innerHTML = opts;
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
    if (!participantes.length) participantes = await api('/participantes');
    if (!fases.length) fases = await api('/fases');

    const filtroPart = document.getElementById('bet-participant-filter');
    const filtroFase = document.getElementById('bet-phase-filter');

    if (filtroPart.options.length <= 1) 
    {
      participantes.forEach(p => filtroPart.add(new Option(p.nome, p.id)));
    }

    if (filtroFase.options.length <= 1) 
    {
      fases.forEach(f => filtroFase.add(new Option(f.nome, f.id)));
    }

    const pid = filtroPart.value;
    const fid = filtroFase.value;
    let url = '/apostas/?';
    if (pid) url += `id_participante=${pid}&`;

    let apostas = await api(url);
    if (fid) apostas = apostas.filter(a => a.jogo.fase.id == fid);

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

  const p = parseFloat(aposta.pontos);

  if (Math.abs(p) < 0.01)
  {
    return `<span class="pts neutro">= R$ 0,00</span>`;
  }

  if (p > 0)
  {
    return `<span class="pts exact">+R$ ${p.toFixed(2).replace('.',',')} 🎯</span>`;
  }

  return `<span class="pts wrong">-R$ ${Math.abs(p).toFixed(2).replace('.',',')} ✗</span>`;
}

function renderizarApostas(apostas) 
{
  if (!apostas.length) 
  {
    document.getElementById('bets-content').innerHTML = '<div class="empty">Nenhuma aposta encontrada</div>';
    return;
  }

  const porFase = {};
  apostas.forEach(a => 
  {
    const chave = a.jogo.fase.id;
    if (!porFase[chave]) porFase[chave] = { fase: a.jogo.fase, apostas: [] };
    porFase[chave].apostas.push(a);
  });

  let html = '';
  Object.values(porFase).sort((a,b) => a.fase.ordem - b.fase.ordem).forEach(({ fase, apostas: apostasFase }) => {
    html += `<div class="phase-header" style="margin-top:1rem">${fase.nome}</div>`;
    apostasFase.sort((a,b) => new Date(a.jogo.data) - new Date(b.jogo.data)).forEach(aposta => {
      const casa = labelTime(aposta.jogo.time_casa);
      const fora = labelTime(aposta.jogo.time_fora);
      const placarStr = aposta.jogo.encerrado
        ? ` (${aposta.jogo.gols_casa}–${aposta.jogo.gols_fora})` : '';
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
  if (!participantes.length) participantes = await api('/participantes');
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
    toast('Aposta removida');
    carregarApostas();
  } 

  catch(e) 
  { 
    toast('Erro: ' + e.message, true); 
  }
}

carregarPlacar();