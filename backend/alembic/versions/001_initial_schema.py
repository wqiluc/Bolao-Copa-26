"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-11
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "phases",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("slug", sa.String(20), nullable=False, unique=True),
        sa.Column("order", sa.Integer(), nullable=False),
    )

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("flag", sa.String(10)),
    )

    op.create_table(
        "groups",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(2), nullable=False, unique=True),
    )

    op.create_table(
        "participants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
    )

    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("match_number", sa.Integer(), nullable=False, unique=True),
        sa.Column("match_date", sa.DateTime(), nullable=False),
        sa.Column("phase_id", sa.Integer(), sa.ForeignKey("phases.id"), nullable=False),
        sa.Column("group_id", sa.Integer(), sa.ForeignKey("groups.id"), nullable=True),
        sa.Column("home_team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=True),
        sa.Column("away_team_id", sa.Integer(), sa.ForeignKey("teams.id"), nullable=True),
        sa.Column("description", sa.String(200), nullable=True),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
        sa.Column("is_finished", sa.Boolean(), default=False, nullable=False),
    )

    op.create_table(
        "bets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("participant_id", sa.Integer(), sa.ForeignKey("participants.id"), nullable=False),
        sa.Column("match_id", sa.Integer(), sa.ForeignKey("matches.id"), nullable=False),
        sa.Column("predicted_home", sa.Integer(), nullable=False),
        sa.Column("predicted_away", sa.Integer(), nullable=False),
        sa.Column("points_earned", sa.Integer(), default=0, nullable=False),
        sa.UniqueConstraint("participant_id", "match_id", name="uq_bet_participant_match"),
    )


def downgrade() -> None:
    op.drop_table("bets")
    op.drop_table("matches")
    op.drop_table("participants")
    op.drop_table("groups")
    op.drop_table("teams")
    op.drop_table("phases")
