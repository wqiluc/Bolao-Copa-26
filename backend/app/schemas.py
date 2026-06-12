from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PhaseOut(BaseModel):
    id: int
    name: str
    slug: str
    order: int
    bet_value: float
    model_config = {"from_attributes": True}


class TeamOut(BaseModel):
    id: int
    name: str
    flag: Optional[str]
    model_config = {"from_attributes": True}


class GroupOut(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class ParticipantOut(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class MatchOut(BaseModel):
    id: int
    match_number: int
    match_date: datetime
    phase: PhaseOut
    group: Optional[GroupOut]
    home_team: Optional[TeamOut]
    away_team: Optional[TeamOut]
    description: Optional[str]
    home_score: Optional[int]
    away_score: Optional[int]
    is_finished: bool
    model_config = {"from_attributes": True}


class MatchResultIn(BaseModel):
    home_score: int
    away_score: int


class MatchUpdateTeams(BaseModel):
    home_team_id: int
    away_team_id: int


class BetIn(BaseModel):
    participant_id: int
    match_id: int
    predicted_home: int
    predicted_away: int


class BetUpdate(BaseModel):
    predicted_home: int
    predicted_away: int


class BetOut(BaseModel):
    id: int
    participant: ParticipantOut
    match: MatchOut
    predicted_home: int
    predicted_away: int
    amount: float
    points_earned: int
    model_config = {"from_attributes": True}


class PhaseScore(BaseModel):
    phase: PhaseOut
    points: int

class ParticipantScore(BaseModel):
    participant: ParticipantOut
    total_points: int
    exact_scores: int
    correct_outcomes: int
    total_spent: float
    by_phase: list[PhaseScore]