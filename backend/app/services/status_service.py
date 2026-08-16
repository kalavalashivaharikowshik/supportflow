from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants import (
    AuditEventType,
    NotificationType,
    TicketStatus,
)
from app.models.ticket import Ticket
from app.models.user import User
from app.repositories.ticket_repository import save_ticket
from app.services.app_config_service import (
    get_or_create_app_config,
)
from app.services.audit_service import (
    record_audit_event,
)
from app.services.notification_service import (
    notify_user,
)
from app.utils.datetime import utc_now


def start_ticket_work(
    db: Session,
    *,
    ticket: Ticket,
    agent: User,
) -> Ticket:
    if ticket.assigned_agent_id != agent.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the assigned agent can start work on this ticket.",
        )

    if ticket.status not in {
        TicketStatus.ASSIGNED.value,
        TicketStatus.REOPENED.value,
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Ticket can only be moved to IN_PROGRESS "
                "from ASSIGNED or REOPENED."
            ),
        )

    old_status = ticket.status

    ticket.status = TicketStatus.IN_PROGRESS.value

    ticket = save_ticket(
        db,
        ticket,
    )

    record_audit_event(
        db,
        ticket=ticket,
        actor=agent,
        event_type=AuditEventType.WORK_STARTED,
        description=(
            f"{agent.full_name} started "
            "working on the ticket."
        ),
        old_value=old_status,
        new_value=TicketStatus.IN_PROGRESS.value,
    )

    return ticket


def resolve_ticket(
    db: Session,
    *,
    ticket: Ticket,
    agent: User,
    resolution_summary: str,
) -> Ticket:
    if ticket.assigned_agent_id != agent.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the assigned agent can resolve this ticket.",
        )

    if ticket.status not in {
        TicketStatus.IN_PROGRESS.value,
        TicketStatus.ESCALATED.value,
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only IN_PROGRESS or ESCALATED "
                "tickets can be resolved."
            ),
        )
    old_status = ticket.status
    now = utc_now()

    ticket.status = TicketStatus.RESOLVED.value
    ticket.resolution_summary = resolution_summary
    ticket.resolved_at = now
    ticket.closed_at = None

    ticket = save_ticket(
        db,
        ticket,
    )

    record_audit_event(
        db,
        ticket=ticket,
        actor=agent,
        event_type=AuditEventType.TICKET_RESOLVED,
        description=(
            f"Ticket resolved by "
            f"{agent.full_name}."
        ),
        old_value=old_status,
        new_value=TicketStatus.RESOLVED.value,
    )
    notify_user(
        db,
        user_id=ticket.requester_id,
        notification_type=(
            NotificationType.TICKET_RESOLVED
        ),
        title="Ticket resolved",
        message=(
            f"{ticket.ticket_number} "
            "has been marked as resolved."
        ),
        ticket_id=ticket.id,
    )

    return ticket


def close_ticket(
    db: Session,
    *,
    ticket: Ticket,
    requester: User,
) -> Ticket:
    if ticket.requester_id != requester.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the ticket requester can close this ticket.",
        )

    if ticket.status != TicketStatus.RESOLVED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only resolved tickets can be closed.",
        )

    old_status = ticket.status
    ticket.status = TicketStatus.CLOSED.value
    ticket.closed_at = utc_now()

    ticket = save_ticket(
        db,
        ticket,
    )

    record_audit_event(
        db,
        ticket=ticket,
        actor=requester,
        event_type=AuditEventType.TICKET_CLOSED,
        description=(
            f"Ticket closed by "
            f"{requester.full_name}."
        ),
        old_value=old_status,
        new_value=TicketStatus.CLOSED.value,
    )
    if ticket.assigned_agent_id is not None:
        notify_user(
            db,
            user_id=ticket.assigned_agent_id,
            notification_type=(
                NotificationType.TICKET_CLOSED
            ),
            title="Ticket closed",
            message=(
                f"{ticket.ticket_number} "
                "has been closed by the requester."
            ),
            ticket_id=ticket.id,
        )

    return ticket


def reopen_ticket(
    db: Session,
    *,
    ticket: Ticket,
    requester: User,
) -> Ticket:
    if ticket.requester_id != requester.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the ticket requester can reopen this ticket.",
        )
    config = get_or_create_app_config(
        db
    )

    if not config.allow_requester_reopen:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Ticket reopening is currently disabled."
            ),
        )

    if ticket.status != TicketStatus.RESOLVED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only resolved tickets can be reopened.",
        )

    old_status = ticket.status
    ticket.status = TicketStatus.REOPENED.value

    ticket.resolved_at = None
    ticket.closed_at = None
    ticket.resolution_summary = None

    ticket = save_ticket(
        db,
        ticket,
    )

    record_audit_event(
        db,
        ticket=ticket,
        actor=requester,
        event_type=AuditEventType.TICKET_REOPENED,
        description=(
            f"Ticket reopened by "
            f"{requester.full_name}."
        ),
        old_value=old_status,
        new_value=TicketStatus.REOPENED.value,
    )
    if ticket.assigned_agent_id is not None:
        notify_user(
            db,
            user_id=ticket.assigned_agent_id,
            notification_type=(
                NotificationType.TICKET_REOPENED
            ),
            title="Ticket reopened",
            message=(
                f"{ticket.ticket_number} "
                "has been reopened by the requester."
            ),
            ticket_id=ticket.id,
        )

    return ticket