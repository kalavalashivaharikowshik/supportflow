from sqlalchemy.orm import Session

from app.core.constants import AuditEventType, UserRole
from app.models.ticket import Ticket
from app.models.ticket_audit import TicketAudit
from app.models.user import User
from app.repositories.audit_repository import (
    create_audit_entry,
    list_ticket_audits,
)
from app.schemas.ticket_audit import (
    TicketAuditItem,
    TicketAuditTimelineResponse,
)


def record_audit_event(
    db: Session,
    *,
    ticket: Ticket,
    event_type: AuditEventType,
    description: str,
    actor: User | None = None,
    old_value: str | None = None,
    new_value: str | None = None,
    is_internal: bool = False,
) -> TicketAudit:
    audit = TicketAudit(
        ticket_id=ticket.id,
        actor_id=(
            actor.id
            if actor is not None
            else None
        ),
        event_type=event_type.value,
        old_value=old_value,
        new_value=new_value,
        description=description,
        is_internal=is_internal,
    )

    return create_audit_entry(
        db,
        audit,
    )


def build_audit_item(
    audit: TicketAudit,
) -> TicketAuditItem:
    if audit.actor is None:
        actor_name = "SYSTEM"
        actor_role = None
    else:
        actor_name = audit.actor.full_name
        actor_role = audit.actor.role.name

    return TicketAuditItem(
        id=audit.id,
        ticket_id=audit.ticket_id,
        actor_id=audit.actor_id,
        actor_name=actor_name,
        actor_role=actor_role,
        event_type=AuditEventType(
            audit.event_type
        ),
        old_value=audit.old_value,
        new_value=audit.new_value,
        description=audit.description,
        is_internal=audit.is_internal,
        created_at=audit.created_at,
    )


def get_ticket_audit_timeline(
    db: Session,
    *,
    ticket: Ticket,
    user: User,
) -> TicketAuditTimelineResponse:
    include_internal = (
        user.role.name
        in {
            UserRole.AGENT.value,
            UserRole.ADMIN.value,
        }
    )

    audits = list_ticket_audits(
        db,
        ticket_id=ticket.id,
        include_internal=include_internal,
    )

    return TicketAuditTimelineResponse(
        items=[
            build_audit_item(audit)
            for audit in audits
        ],
        total=len(audits),
    )