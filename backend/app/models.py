from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, UniqueConstraint, Numeric
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Phase(Base):
    __tablename__ = "phases"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    slug = Column(String(20), nullable=False, unique=True)
    order = Column(Integer, nullable=False)
    bet_value = Column(Numeric(10, 2), nullable=False, default=1)

    matches = relationship("Match", back_populates="phase")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    flag = Column(String(10))

    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(2), nullable=False, unique=True)

    matches = relationship("Match", back_populates="group")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    match_number = Column(Integer, nullable=False, unique=True)
    match_date = Column(DateTime, nullable=False)
    phase_id = Column(Integer, ForeignKey("phases.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    description = Column(String(200), nullable=True)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    is_finished = Column(Boolean, default=False, nullable=False)

    phase = relationship("Phase", back_populates="matches")
    group = relationship("Group", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    bets = relationship("Bet", back_populates="match")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

    bets = relationship("Bet", back_populates="participant")


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    predicted_home = Column(Integer, nullable=False)
    predicted_away = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False, default=1)
    points_earned = Column(Integer, default=0, nullable=False)

    __table_args__ = (UniqueConstraint("participant_id", "match_id", name="uq_bet_participant_match"),)

    participant = relationship("Participant", back_populates="bets")
    match = relationship("Match", back_populates="bets")
