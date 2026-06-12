from sqlalchemy.orm import Session
from . import models


def _outcome(home: int, away: int) -> str:
    if home > away:
        return "H"
    if away > home:
        return "A"
    return "D"


def calculate_points(predicted_home: int, predicted_away: int, actual_home: int, actual_away: int) -> int:
    if predicted_home == actual_home and predicted_away == actual_away:
        return 3
    if _outcome(predicted_home, predicted_away) == _outcome(actual_home, actual_away):
        return 1
    return 0


def recalculate_match_bets(db: Session, match: models.Match) -> None:
    if not match.is_finished or match.home_score is None or match.away_score is None:
        return
    for bet in match.bets:
        bet.points_earned = calculate_points(
            bet.predicted_home, bet.predicted_away,
            match.home_score, match.away_score,
        )
    db.commit()


def set_match_result(db: Session, match_id: int, home_score: int, away_score: int) -> models.Match | None:
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        return None
    match.home_score = home_score
    match.away_score = away_score
    match.is_finished = True
    db.commit()
    db.refresh(match)
    recalculate_match_bets(db, match)
    return match


def get_scores(db: Session) -> list[dict]:
    participants = db.query(models.Participant).all()
    phases = db.query(models.Phase).order_by(models.Phase.order).all()
    result = []
    for p in participants:
        by_phase = []
        total = 0
        exact = 0
        correct = 0
        total_spent = float(sum(b.amount for b in p.bets))
        for phase in phases:
            pts = sum(
                b.points_earned
                for b in p.bets
                if b.match.phase_id == phase.id and b.match.is_finished
            )
            by_phase.append({"phase": phase, "points": pts})
            total += pts
            for b in p.bets:
                if b.match.phase_id == phase.id and b.match.is_finished:
                    if b.points_earned == 3:
                        exact += 1
                    elif b.points_earned == 1:
                        correct += 1
        result.append({
            "participant": p,
            "total_points": total,
            "exact_scores": exact,
            "correct_outcomes": correct,
            "total_spent": total_spent,
            "by_phase": by_phase,
        })
    result.sort(key=lambda x: (-x["total_points"], -x["exact_scores"], -x["correct_outcomes"]))
    return result
