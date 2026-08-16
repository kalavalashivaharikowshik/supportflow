from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.api.dependencies.permissions import (
    require_admin,
)
from app.core.constants import TicketPriority
from app.db.database import get_db
from app.models.user import User
from app.schemas.sla import (
    EscalationScanResponse,
    SLAConfigResponse,
    SLAConfigUpdateRequest,
)
from app.services.escalation_service import (
    process_sla_escalations,
)
from app.services.sla_service import (
    build_sla_config_response,
    get_all_sla_configs,
    update_sla_config,
)

router = APIRouter(
    prefix="/sla",
    tags=["SLA"],
)


@router.get(
    "/configs",
    response_model=list[SLAConfigResponse],
)
def list_configs(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    del admin

    return get_all_sla_configs(
        db
    )


@router.patch(
    "/configs/{priority}",
    response_model=SLAConfigResponse,
)
def update_config(
    priority: TicketPriority,
    payload: SLAConfigUpdateRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    del admin

    config = update_sla_config(
        db,
        priority=priority,
        resolution_minutes=(
            payload.resolution_minutes
        ),
        is_active=payload.is_active,
    )

    return build_sla_config_response(
        config
    )

@router.post(
    "/escalations/run",
    response_model=EscalationScanResponse,
)
def run_escalation_scan(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    del admin

    tickets = process_sla_escalations(
        db
    )

    return EscalationScanResponse(
        escalated_count=len(tickets),
        ticket_ids=[
            ticket.id
            for ticket in tickets
        ],
        ticket_numbers=[
            ticket.ticket_number
            for ticket in tickets
        ],
    )