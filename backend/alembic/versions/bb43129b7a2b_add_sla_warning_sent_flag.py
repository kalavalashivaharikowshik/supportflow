"""add sla warning sent flag

Revision ID: bb43129b7a2b
Revises: 8acb15f1d05e
Create Date: 2026-08-15 02:45:56.195188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb43129b7a2b'
down_revision: Union[str, Sequence[str], None] = '8acb15f1d05e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "tickets",
        sa.Column(
            "sla_warning_sent",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.create_index(
        op.f("ix_tickets_sla_warning_sent"),
        "tickets",
        ["sla_warning_sent"],
        unique=False,
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_tickets_sla_warning_sent"),
        table_name="tickets",
    )

    op.drop_column(
        "tickets",
        "sla_warning_sent",
    )