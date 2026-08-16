from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants import TicketPriority
from app.models.sla_config import SLAConfig
from app.models.ticket import Ticket
from app.repositories.sla_repository import (
    get_sla_config_by_priority,
    list_sla_configs,
    save_sla_config,
)
from app.schemas.sla import (
    SLAConfigResponse,
    TicketSLAStatusResponse,
)


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    )


def normalize_datetime(
    value: datetime,
) -> datetime:
    if value.tzinfo is None:
        return value.replace(
            tzinfo=timezone.utc,
        )

    return value.astimezone(
        timezone.utc
    )


def build_sla_config_response(
    config: SLAConfig,
) -> SLAConfigResponse:
    return SLAConfigResponse(
        id=config.id,
        priority=TicketPriority(
            config.priority
        ),
        resolution_minutes=(
            config.resolution_minutes
        ),
        is_active=config.is_active,
        created_at=config.created_at,
        updated_at=config.updated_at,
    )


def get_active_sla_config(
    db: Session,
    priority: TicketPriority,
) -> SLAConfig:
    config = get_sla_config_by_priority(
        db,
        priority.value,
    )

    if config is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                f"SLA configuration for "
                f"{priority.value} is missing."
            ),
        )

    if not config.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"SLA configuration for "
                f"{priority.value} is inactive."
            ),
        )

    return config


def calculate_sla_deadline(
    db: Session,
    *,
    priority: TicketPriority,
    created_at: datetime,
) -> datetime:
    config = get_active_sla_config(
        db,
        priority,
    )

    return normalize_datetime(
        created_at
    ) + timedelta(
        minutes=config.resolution_minutes,
    )


def get_all_sla_configs(
    db: Session,
) -> list[SLAConfigResponse]:
    configs = list_sla_configs(
        db
    )

    return [
        build_sla_config_response(
            config
        )
        for config in configs
    ]


def update_sla_config(
    db: Session,
    *,
    priority: TicketPriority,
    resolution_minutes: int,
    is_active: bool,
) -> SLAConfig:
    config = get_sla_config_by_priority(
        db,
        priority.value,
    )

    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA configuration not found.",
        )

    config.resolution_minutes = (
        resolution_minutes
    )

    config.is_active = is_active

    return save_sla_config(
        db,
        config,
    )


def calculate_ticket_sla_status(
    ticket: Ticket,
) -> TicketSLAStatusResponse:
    now = utc_now()

    created_at = normalize_datetime(
        ticket.created_at
    )

    deadline = normalize_datetime(
        ticket.sla_deadline
    )

    total_seconds = max(
        int(
            (
                deadline - created_at
            ).total_seconds()
        ),
        1,
    )

    elapsed_seconds = max(
        int(
            (
                now - created_at
            ).total_seconds()
        ),
        0,
    )

    remaining_seconds = int(
        (
            deadline - now
        ).total_seconds()
    )

    is_breached = (
        now >= deadline
    )

    percentage_consumed = (
        elapsed_seconds
        / total_seconds
    ) * 100

    percentage_consumed = round(
        percentage_consumed,
        2,
    )

    is_at_risk = (
        not is_breached
        and percentage_consumed >= 80
    )

    return TicketSLAStatusResponse(
        ticket_id=ticket.id,
        ticket_number=ticket.ticket_number,
        priority=TicketPriority(
            ticket.priority
        ),
        created_at=created_at,
        sla_deadline=deadline,
        is_breached=is_breached,
        remaining_seconds=remaining_seconds,
        elapsed_seconds=elapsed_seconds,
        total_sla_seconds=total_seconds,
        percentage_consumed=percentage_consumed,
        is_at_risk=is_at_risk,
    )