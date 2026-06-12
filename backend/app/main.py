from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_db, engine
from . import models, schemas
from .routers import matches, bets, scores

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bolão Copa do Mundo 2026", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matches.router, prefix="/api")
app.include_router(bets.router, prefix="/api")
app.include_router(scores.router, prefix="/api")


@app.get("/api/phases", response_model=list[schemas.PhaseOut])
def list_phases(db: Session = Depends(get_db)):
    return db.query(models.Phase).order_by(models.Phase.order).all()


@app.get("/api/teams", response_model=list[schemas.TeamOut])
def list_teams(db: Session = Depends(get_db)):
    return db.query(models.Team).order_by(models.Team.name).all()


@app.get("/api/groups", response_model=list[schemas.GroupOut])
def list_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).order_by(models.Group.name).all()


@app.get("/api/participants", response_model=list[schemas.ParticipantOut])
def list_participants(db: Session = Depends(get_db)):
    return db.query(models.Participant).order_by(models.Participant.name).all()


@app.get("/health")
def health():
    return {"status": "ok"}
