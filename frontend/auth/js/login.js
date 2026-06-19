const API = '/api';

function toast(mensagem, erro = false) 
{
  const elementoToast = document.getElementById('toast');
  elementoToast.textContent = mensagem;
  elementoToast.className = 'toast show' + (erro ? ' error' : '');

  setTimeout
  (
    () => { elementoToast.className = 'toast'; }, 3000
  );
}

async function realizarLogin(evento) 
{
  evento.preventDefault();

  const nome = document.getElementById('campo-nome').value.trim();
  const senha = document.getElementById('campo-senha').value;
  const botao = document.getElementById('btn-entrar');

  botao.disabled = true;
  botao.textContent = 'Entrando...';

  try 
  {
    const resposta = await fetch(API + '/auth/login', 
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nome, senha }),
    });

    if (!resposta.ok) 
    {
      const erro = await resposta.json().catch(() => ({}));
      throw new Error (erro.detail || 'Erro ao fazer login no app ❌.');
    }

    const participante = await resposta.json();

    localStorage.setItem('participante_auth', JSON.stringify(participante));
    localStorage.setItem('recem_logado', '1');

    toast(`Bem-vindo de volta, ${participante.nome}!`);
    setTimeout(() => { window.location.href = '/'; }, 1400);

  } 

  catch (e) 
  {
    toast(e.message, true);
    botao.disabled = false;
    botao.textContent = 'Entrar';
  }
}