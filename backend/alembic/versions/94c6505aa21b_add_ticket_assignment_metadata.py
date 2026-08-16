"""add ticket assignment metadata

Revision ID: 94c6505aa21b
Revises: da9d211502ac
Create Date: 2026-08-12 23:39:30.638485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94c6505aa21b'
down_revision: Union[str, Sequence[str], None] = 'da9d211502ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("tickets") as batch_op:
        batch_op.add_column(
            sa.Column(
                "assigned_at",
                sa.DateTime(timezone=True),
                nullable=True,
            )
        )

        batch_op.add_column(
            sa.Column(
                "assigned_by_id",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.create_index(
            "ix_tickets_assigned_by_id",
            ["assigned_by_id"],
            unique=False,
        )

        batch_op.create_foreign_key(
            "fk_tickets_assigned_by_id_users",
            "users",
            ["assigned_by_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("tickets") as batch_op:
        batch_op.drop_constraint(
            "fk_tickets_assigned_by_id_users",
            type_="foreignkey",
        )

        batch_op.drop_index(
            "ix_tickets_assigned_by_id",
        )

        batch_op.drop_column(
            "assigned_by_id",
        )

        batch_op.drop_column(
            "assigned_at",
        )