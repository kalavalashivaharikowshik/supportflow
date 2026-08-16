from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AppConfig(Base):
    __tablename__ = "app_configs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    sla_warning_threshold_percent: Mapped[int] = mapped_column(
        Integer,
        default=80,
        nullable=False,
    )

    escalation_check_interval_seconds: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )

    max_active_tickets_per_agent: Mapped[int] = mapped_column(
        Integer,
        default=20,
        nullable=False,
    )

    auto_reassign_on_escalation: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    allow_requester_reopen: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    allow_admin_public_response: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    notifications_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    websocket_notifications_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )