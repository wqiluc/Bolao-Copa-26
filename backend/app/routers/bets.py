from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/bets", tags=["bets"])


def _load_bet(db: Session, bet_id: int) -> models.Bet:
    bet = (
        db.query(models.Bet)
        .options(
            joinedload(models.Bet.participant),
            joinedload(models.Bet.match).joinedload(models.Match.phase),
            joinedload(models.Bet.match).joinedload(models.Match.group),
            joinedload(models.Bet.match).joinedload(models.Match.home_team),
            joinedload(models.Bet.match).joinedload(models.Match.away_team),
        )
        .filter(models.Bet.id == bet_id)
        .first()
    )
    if not bet:
        raise HTTPException(status_code=404, detail="Aposta não encontrada")
    return bet


@router.get("/", response_model=list[schemas.BetOut])
def list_bets(
    participant_id: Optional[int] = None,
    match_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Bet).options(
        joinedload(models.Bet.participant),
        joinedload(models.Bet.match).joinedload(models.Match.phase),
        joinedload(models.Bet.match).joinedload(models.Match.group),
        joinedload(models.Bet.match).joinedload(models.Match.home_team),
        joinedload(models.Bet.match).joinedload(models.Match.away_team),
    )
    if participant_id:
        q = q.filter(models.Bet.participant_id == participant_id)
    if match_id:
        q = q.filter(models.Bet.match_id == match_id)
    return q.all()


@router.post("/", response_model=schemas.BetOut, status_code=201)
def create_bet(body: schemas.BetIn, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == body.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    if match.is_finished:
        raise HTTPException(status_code=400, detail="Jogo já encerrado, não é possível apostar")

    phase = db.query(models.Phase).filter(models.Phase.id == match.phase_id).first()
    bet = models.Bet(
        participant_id=body.participant_id,
        match_id=body.match_id,
        predicted_home=body.predicted_home,
        predicted_away=body.predicted_away,
        amount=phase.bet_value,
    )
    db.add(bet)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Aposta já registrada para este jogo/participante")
    db.refresh(bet)
    return _load_bet(db, bet.id)


@router.put("/{bet_id}", response_model=schemas.BetOut)
def update_bet(bet_id: int, body: schemas.BetUpdate, db: Session = Depends(get_db)):
    bet = db.query(models.Bet).filter(models.Bet.id == bet_id).first()
    if not bet:
        raise HTTPException(status_code=404, detail="Aposta não encontrada")
    if bet.match.is_finished:
        raise HTTPException(status_code=400, detail="Jogo já encerrado, não é possível alterar aposta")
    bet.predicted_home = body.predicted_home
    bet.predicted_away = body.predicted_away
    db.commit()
    return _load_bet(db, bet_id)


@router.delete("/{bet_id}", status_code=204)
def delete_bet(bet_id: int, db: Session = Depends(get_db)):
    bet = db.query(models.Bet).filter(models.Bet.id == bet_id).first()
    if not bet:
        raise HTTPException(status_code=404, detail="Aposta não encontrada")
    if bet.match.is_finished:
        raise HTTPException(status_code=400, detail="Jogo já encerrado, não é possível remover aposta")
    db.delete(bet)
    db.commit()
