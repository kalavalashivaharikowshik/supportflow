from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_user,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.ticket_audit import (
    TicketAuditTimelineResponse,
)
from app.services.audit_service import (
    get_ticket_audit_timeline,
)
from app.services.ticket_service import (
    get_accessible_ticket,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Ticket Audit"],
)


@router.get(
    "/{ticket_id}/audit",
    response_model=TicketAuditTimelineResponse,
)
def get_ticket_audit(
    ticket_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    ticket = get_accessible_ticket(
        db,
        user=current_user,
        ticket_id=ticket_id,
    )

    return get_ticket_audit_timeline(
        db,
        ticket=ticket,
        user=current_user,
    )