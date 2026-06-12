from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UniqueConstraint, Numeric
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Fase(Base):
    __tablename__ = "fases"

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    slug = Column(String(20), nullable=False, unique=True)
    ordem = Column(Integer, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False, default=1)

    jogos = relationship("Jogo", back_populates="fase")


class Time(Base):
    __tablename__ = "times"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    bandeira = Column(String(10))

    jogos_casa = relationship("Jogo", foreign_keys="Jogo.id_time_casa", back_populates="time_casa")
    jogos_fora = relationship("Jogo", foreign_keys="Jogo.id_time_fora", back_populates="time_fora")


class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(2), nullable=False, unique=True)

    jogos = relationship("Jogo", back_populates="grupo")


class Jogo(Base):
    __tablename__ = "jogos"

    id = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False, unique=True)
    data = Column(DateTime, nullable=False)
    id_fase = Column(Integer, ForeignKey("fases.id"), nullable=False)
    id_grupo = Column(Integer, ForeignKey("grupos.id"), nullable=True)
    id_time_casa = Column(Integer, ForeignKey("times.id"), nullable=True)
    id_time_fora = Column(Integer, ForeignKey("times.id"), nullable=True)
    descricao = Column(String(200), nullable=True)
    local = Column(String(100), nullable=True)
    gols_casa = Column(Integer, nullable=True)
    gols_fora = Column(Integer, nullable=True)
    encerrado = Column(Boolean, default=False, nullable=False)

    fase = relationship("Fase", back_populates="jogos")
    grupo = relationship("Grupo", back_populates="jogos")
    time_casa = relationship("Time", foreign_keys=[id_time_casa], back_populates="jogos_casa")
    time_fora = relationship("Time", foreign_keys=[id_time_fora], back_populates="jogos_fora")
    apostas = relationship("Aposta", back_populates="jogo")


class Participante(Base):
    __tablename__ = "participantes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)

    apostas = relationship("Aposta", back_populates="participante")


class Aposta(Base):
    __tablename__ = "apostas"

    id = Column(Integer, primary_key=True)
    id_participante = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    id_jogo = Column(Integer, ForeignKey("jogos.id"), nullable=False)
    palpite_casa = Column(Integer, nullable=False)
    palpite_fora = Column(Integer, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False, default=1)
    pontos = Column(Numeric(10, 2), default=0, nullable=False)

    __table_args__ = (UniqueConstraint("id_participante", "id_jogo", name="uq_aposta_participante_jogo"),)

    participante = relationship("Participante", back_populates="apostas")
    jogo = relationship("Jogo", back_populates="apostas")