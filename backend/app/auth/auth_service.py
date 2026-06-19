from passlib.context import CryptContext
from sqlalchemy.orm import Session
import app.modelos as modelos

RODADAS_SALT = 12

_contexto_cripto = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=RODADAS_SALT,
    deprecated="auto",
)

def criar_hash_senha(senha: str) -> str:
    return _contexto_cripto.hash(senha)

def verificar_senha(senha: str, hash_armazenado: str) -> bool:
    return _contexto_cripto.verify(senha, hash_armazenado)

def autenticar_participante(bd: Session, nome: str, senha: str):
    participante = (
        bd.query(modelos.Participante)
        .filter(modelos.Participante.nome == nome)
        .first()
    )
    
    if (not participante) or (not participante.senha_hash):
        return None
    
    if (not verificar_senha(senha, participante.senha_hash)):
        return None

    return participante