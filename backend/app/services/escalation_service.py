from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.constants import (
    AuditEventType,
    NotificationType,
    TicketStatus,
)
from app.models.ticket import Ticket
from app.repositories.ticket_repository import (
    list_escalation_candidates,
    list_sla_warning_candidates,
    save_ticket,
)
from app.repositories.user_repository import (
    get_user_by_id,
    list_active_admins,
)
from app.services.app_config_service import (
    get_or_create_app_config,
)
from app.services.assignment_service import (
    find_best_replacement_agent,
)
from app.services.audit_service import (
    record_audit_event,
)
from app.services.notification_service import (
    notify_user,
)

ESCALATABLE_STATUSES = {
    TicketStatus.OPEN.value,
    TicketStatus.ASSIGNED.value,
    TicketStatus.IN_PROGRESS.value,
    TicketStatus.REOPENED.value,
}


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


def should_escalate_ticket(
    ticket: Ticket,
    *,
    now: datetime,
) -> bool:
    if ticket.is_escalated:
        return False

    if ticket.status not in ESCALATABLE_STATUSES:
        return False

    deadline = normalize_datetime(
        ticket.sla_deadline
    )

    current_time = normalize_datetime(
        now
    )

    return current_time >= deadline


def auto_reassign_ticket_after_escalation(
    db: Session,
    *,
    ticket: Ticket,
) -> Ticket:
    if ticket.assigned_agent_id is None:
        return ticket

    app_config = get_or_create_app_config(
        db
    )

    if not app_config.auto_reassign_on_escalation:
        return ticket

    old_agent_id = (
        ticket.assigned_agent_id
    )

    replacement_agent = (
        find_best_replacement_agent(
            db,
            current_agent_id=old_agent_id,
        )
    )

    if replacement_agent is None:
        return ticket

    old_agent = get_user_by_id(
        db,
        old_agent_id,
    )

    ticket.assigned_agent_id = (
        replacement_agent.id
    )

    ticket.assigned_at = utc_now()

    ticket = save_ticket(
        db,
        ticket,
    )

    record_audit_event(
        db,
        ticket=ticket,
        actor=None,
        event_type=(
            AuditEventType.TICKET_REASSIGNED
        ),
        description=(
            "Ticket automatically reassigned "
            f"from {old_agent.full_name} "
            f"to {replacement_agent.full_name} "
            "after SLA breach."
        ),
        old_value=(
            f"{old_agent.id}:{old_agent.full_name}"
        ),
        new_value=(
            f"{replacement_agent.id}:"
            f"{replacement_agent.full_name}"
        ),
    )

    notify_user(
        db,
        user_id=old_agent.id,
        notification_type=(
            NotificationType.TICKET_REASSIGNED
        ),
        title=(
            "Ticket reassigned after SLA breach"
        ),
        message=(
            f"{ticket.ticket_number} "
            "was automatically reassigned "
            "to another agent after "
            "an SLA breach."
        ),
        ticket_id=ticket.id,
    )

    notify_user(
        db,
        user_id=replacement_agent.id,
        notification_type=(
            NotificationType.TICKET_REASSIGNED
        ),
        title=(
            "Escalated ticket assigned to you"
        ),
        message=(
            f"{ticket.ticket_number} "
            "was automatically assigned "
            "to you after an SLA breach."
        ),
        ticket_id=ticket.id,
    )

    return ticket

def escalate_ticket(
    db: Session,
    *,
    ticket: Ticket,
    now: datetime | None = None,
) -> Ticket:
    current_time = (
        now
        if now is not None
        else utc_now()
    )

    if not should_escalate_ticket(
        ticket,
        now=current_time,
    ):
        return ticket

    ticket.is_escalated = True
    ticket.escalated_at = (
        normalize_datetime(
            current_time
        )
    )
    old_status = ticket.status
    ticket.status = (
        TicketStatus.ESCALATED.value
    )

    ticket = save_ticket(
        db,
        ticket,
    )
    record_audit_event(
        db,
        ticket=ticket,
        actor=None,
        event_type=(
            AuditEventType.SLA_ESCALATED
        ),
        description=(
            "Ticket automatically escalated "
            "after SLA breach."
        ),
        old_value=old_status,
        new_value=TicketStatus.ESCALATED.value,
    )
    ticket = (
        auto_reassign_ticket_after_escalation(
            db,
            ticket=ticket,
        )
    )
    if ticket.assigned_agent_id is not None:
        notify_user(
            db,
            user_id=ticket.assigned_agent_id,
            notification_type=(
                NotificationType.SLA_ESCALATED
            ),
            title="SLA breached",
            message=(
                f"{ticket.ticket_number} "
                "has breached its SLA and was escalated."
            ),
            ticket_id=ticket.id,
        )
    admins = list_active_admins(
        db
    )

    for admin in admins:
        notify_user(
            db,
            user_id=admin.id,
            notification_type=(
                NotificationType.SLA_ESCALATED
            ),
            title="SLA escalation",
            message=(
                f"{ticket.ticket_number} "
                "has breached its SLA."
            ),
            ticket_id=ticket.id,
        )

    return ticket


def process_sla_escalations(
    db: Session,
    *,
    now: datetime | None = None,
) -> list[Ticket]:
    current_time = (
        now
        if now is not None
        else utc_now()
    )

    candidates = (
        list_escalation_candidates(
            db,
            now=current_time,
        )
    )

    escalated_tickets: list[Ticket] = []

    for ticket in candidates:
        if should_escalate_ticket(
            ticket,
            now=current_time,
        ):
            escalated_ticket = (
                escalate_ticket(
                    db,
                    ticket=ticket,
                    now=current_time,
                )
            )

            escalated_tickets.append(
                escalated_ticket
            )

    return escalated_tickets

def process_sla_warnings(
    db: Session,
    *,
    now: datetime | None = None,
) -> list[Ticket]:
    current_time = (
        now
        if now is not None
        else utc_now()
    )
    app_config = get_or_create_app_config(
        db
    )

    warning_threshold = (
        app_config.sla_warning_threshold_percent
    )

    candidates = list_sla_warning_candidates(
        db,
        now=current_time,
    )

    warned_tickets: list[Ticket] = []

    for ticket in candidates:
        created_at = normalize_datetime(
            ticket.created_at
        )

        deadline = normalize_datetime(
            ticket.sla_deadline
        )

        total_seconds = (
            deadline - created_at
        ).total_seconds()

        elapsed_seconds = (
            normalize_datetime(
                current_time
            )
            - created_at
        ).total_seconds()

        if total_seconds <= 0:
            continue

        percentage = (
            elapsed_seconds
            / total_seconds
        ) * 100

        if percentage < warning_threshold:
            continue

        ticket.sla_warning_sent = True

        ticket = save_ticket(
            db,
            ticket,
        )

        if ticket.assigned_agent_id is not None:
            notify_user(
                db,
                user_id=ticket.assigned_agent_id,
                notification_type=(
                    NotificationType.SLA_AT_RISK
                ),
                title="Ticket approaching SLA",
                message=(
                    f"{ticket.ticket_number} "
                    f"has consumed at least "
                    f"{warning_threshold}%"
                    "of its SLA window."
                ),
                ticket_id=ticket.id,
            )

        admins = list_active_admins(
            db
        )

        for admin in admins:
            notify_user(
                db,
                user_id=admin.id,
                notification_type=(
                    NotificationType.SLA_AT_RISK
                ),
                title="Ticket approaching SLA",
                message=(
                    f"{ticket.ticket_number} "
                    f"has consumed at least"
                    f"{warning_threshold}%"
                    "of its SLA window"
                ),
                ticket_id=ticket.id,
            )

        warned_tickets.append(
            ticket
        )

    return warned_tickets