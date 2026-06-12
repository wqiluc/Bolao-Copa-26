from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from .. import models, schemas, crud

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=list[schemas.MatchOut])
def list_matches(
    phase_id: Optional[int] = None,
    group_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Match).options(
        joinedload(models.Match.phase),
        joinedload(models.Match.group),
        joinedload(models.Match.home_team),
        joinedload(models.Match.away_team),
    )
    if phase_id:
        q = q.filter(models.Match.phase_id == phase_id)
    if group_id:
        q = q.filter(models.Match.group_id == group_id)
    return q.order_by(models.Match.match_date, models.Match.match_number).all()


@router.get("/{match_id}", response_model=schemas.MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = (
        db.query(models.Match)
        .options(
            joinedload(models.Match.phase),
            joinedload(models.Match.group),
            joinedload(models.Match.home_team),
            joinedload(models.Match.away_team),
        )
        .filter(models.Match.id == match_id)
        .first()
    )
    if not match:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return match


@router.put("/{match_id}/result", response_model=schemas.MatchOut)
def set_result(match_id: int, body: schemas.MatchResultIn, db: Session = Depends(get_db)):
    match = crud.set_match_result(db, match_id, body.home_score, body.away_score)
    if not match:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    db.refresh(match)
    return db.query(models.Match).options(
        joinedload(models.Match.phase),
        joinedload(models.Match.group),
        joinedload(models.Match.home_team),
        joinedload(models.Match.away_team),
    ).filter(models.Match.id == match_id).first()


@router.put("/{match_id}/teams", response_model=schemas.MatchOut)
def update_teams(match_id: int, body: schemas.MatchUpdateTeams, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    match.home_team_id = body.home_team_id
    match.away_team_id = body.away_team_id
    db.commit()
    return db.query(models.Match).options(
        joinedload(models.Match.phase),
        joinedload(models.Match.group),
        joinedload(models.Match.home_team),
        joinedload(models.Match.away_team),
    ).filter(models.Match.id == match_id).first()
