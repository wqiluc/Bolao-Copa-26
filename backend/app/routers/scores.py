from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud

router = APIRouter(prefix="/scores", tags=["scores"])


@router.get("/", response_model=list[schemas.ParticipantScore])
def get_scores(db: Session = Depends(get_db)):
    raw = crud.get_scores(db)
    return [
        schemas.ParticipantScore(
            participant=schemas.ParticipantOut.model_validate(r["participant"]),
            total_points=r["total_points"],
            exact_scores=r["exact_scores"],
            correct_outcomes=r["correct_outcomes"],
            total_spent=r["total_spent"],
            by_phase=[
                schemas.PhaseScore(
                    phase=schemas.PhaseOut.model_validate(p["phase"]),
                    points=p["points"],
                )
                for p in r["by_phase"]
            ],
        )
        for r in raw
    ]
