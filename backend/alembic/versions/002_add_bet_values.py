"""Add bet_value to phases and amount to bets

Revision ID: 002
Revises: 001
Create Date: 2026-06-11
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("phases", sa.Column("bet_value", sa.Numeric(10, 2), nullable=False, server_default="1"))
    op.add_column("bets",   sa.Column("amount",    sa.Numeric(10, 2), nullable=False, server_default="1"))


def downgrade() -> None:
    op.drop_column("bets",   "amount")
    op.drop_column("phases", "bet_value")
