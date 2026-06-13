from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class FaseSaida(BaseModel):
    id: int
    nome: str
    slug: str
    ordem: int
    valor: float
    model_config = {"from_attributes": True}

class TimeSaida(BaseModel):
    id: int
    nome: str
    bandeira: Optional[str]
    model_config = {"from_attributes": True}

class GrupoSaida(BaseModel):
    id: int
    nome: str
    model_config = {"from_attributes": True}

class ParticipanteSaida(BaseModel):
    id: int
    nome: str
    model_config = {"from_attributes": True}

class JogoSaida(BaseModel):
    id: int
    numero: int
    data: datetime
    fase: FaseSaida
    grupo: Optional[GrupoSaida]
    time_casa: Optional[TimeSaida]
    time_fora: Optional[TimeSaida]
    descricao: Optional[str]
    local: Optional[str]
    gols_casa: Optional[int]
    gols_fora: Optional[int]
    encerrado: bool
    model_config = {"from_attributes": True}

class ResultadoJogo(BaseModel):
    gols_casa: int
    gols_fora: int

class AtualizarTimesJogo(BaseModel):
    id_time_casa: int
    id_time_fora: int

class ApostaEntrada(BaseModel):
    id_participante: int
    id_jogo: int
    palpite_casa: int
    palpite_fora: int

class AtualizarAposta(BaseModel):
    palpite_casa: int
    palpite_fora: int

class ApostaSaida(BaseModel):
    id: int
    participante: ParticipanteSaida
    jogo: JogoSaida
    palpite_casa: int
    palpite_fora: int
    valor: float
    pontos: float
    model_config = {"from_attributes": True}

class PlacarFase(BaseModel):
    fase: FaseSaida
    saldo: float
    ganho: float
    devido: float
    acertos: int

class PlacarParticipante(BaseModel):
    participante: ParticipanteSaida
    saldo_total: float
    total_ganho: float
    total_devido: float
    acertos_exatos: int
    por_fase: list[PlacarFase]