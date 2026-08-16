"""add auto reassign on escalation config

Revision ID: 29b7371875b5
Revises: 41fc37e0107d
Create Date: 2026-08-16 13:30:18.445271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29b7371875b5'
down_revision: Union[str, Sequence[str], None] = '41fc37e0107d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "app_configs",
        sa.Column(
            "auto_reassign_on_escalation",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "app_configs",
        "auto_reassign_on_escalation",
    )