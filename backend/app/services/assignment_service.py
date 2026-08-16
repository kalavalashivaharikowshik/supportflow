from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.constants import (
    AuditEventType,
    NotificationType,
    TicketStatus,
    UserRole,
)
from app.models.ticket import Ticket
from app.models.user import User
from app.repositories.ticket_repository import (
    count_active_agent_tickets,
    save_ticket,
)
from app.repositories.user_repository import (
    get_user_by_id,
)
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


def get_eligible_agent(
    db: Session,
    agent_id: int,
) -> User:
    agent = get_user_by_id(
        db,
        agent_id,
    )

    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found.",
        )

    if not agent.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive users cannot receive tickets.",
        )

    if agent.role.name != UserRole.AGENT.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tickets can only be assigned to agents.",
        )

    return agent


def assign_ticket(
    db: Session,
    *,
    ticket: Ticket,
    agent: User,
    admin: User,
) -> Ticket:
    if ticket.status in {
        TicketStatus.RESOLVED.value,
        TicketStatus.CLOSED.value,
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Resolved or closed tickets "
                "cannot be assigned."
            ),
        )

    if ticket.assigned_agent_id is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Ticket is already assigned. "
                "Use the reassignment endpoint."
            ),
        )

    config = get_or_create_app_config(
        db
    )

    active_count = count_active_agent_tickets(
        db,
        agent_id=agent.id,
    )

    if (
        active_count
        >= config.max_active_tickets_per_agent
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Agent has reached the maximum "
                "active ticket capacity."
            ),
        )

    now = utc_now()

    ticket.assigned_agent_id = agent.id
    ticket.assigned_by_id = admin.id
    ticket.assigned_at = now
    ticket.status = TicketStatus.ASSIGNED.value

    ticket = save_ticket(
        db,
        ticket,
    )

    record_audit_event(
        db,
        ticket=ticket,
        actor=admin,
        event_type=(
            AuditEventType.TICKET_ASSIGNED
        ),
        description=(
            f"Ticket assigned to "
            f"{agent.full_name}."
        ),
        old_value="UNASSIGNED",
        new_value=(
            f"{agent.id}:{agent.full_name}"
        ),
    )

    notify_user(
        db,
        user_id=agent.id,
        notification_type=(
            NotificationType.TICKET_ASSIGNED
        ),
        title="Ticket assigned to you",
        message=(
            f"{ticket.ticket_number} "
            f"has been assigned to you."
        ),
        ticket_id=ticket.id,
    )

    return ticket


def reassign_ticket(
    db: Session,
    *,
    ticket: Ticket,
    agent: User,
    admin: User,
) -> Ticket:
    if ticket.status in {
        TicketStatus.RESOLVED.value,
        TicketStatus.CLOSED.value,
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Resolved or closed tickets "
                "cannot be reassigned."
            ),
        )

    if ticket.assigned_agent_id is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Ticket is not currently assigned. "
                "Use the assignment endpoint."
            ),
        )

    if ticket.assigned_agent_id == agent.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Ticket is already assigned "
                "to this agent."
            ),
        )

    config = get_or_create_app_config(
        db
    )

    active_count = count_active_agent_tickets(
        db,
        agent_id=agent.id,
    )

    if (
        active_count
        >= config.max_active_tickets_per_agent
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Agent has reached the maximum "
                "active ticket capacity."
            ),
        )

    old_agent_id = ticket.assigned_agent_id

    old_agent = get_user_by_id(
        db,
        old_agent_id,
    )

    ticket.assigned_agent_id = agent.id
    ticket.assigned_by_id = admin.id
    ticket.assigned_at = utc_now()

    if ticket.status == TicketStatus.OPEN.value:
        ticket.status = TicketStatus.ASSIGNED.value

    ticket = save_ticket(
        db,
        ticket,
    )

    record_audit_event(
        db,
        ticket=ticket,
        actor=admin,
        event_type=(
            AuditEventType.TICKET_REASSIGNED
        ),
        description=(
            f"Ticket reassigned from "
            f"{old_agent.full_name} "
            f"to {agent.full_name}."
        ),
        old_value=(
            f"{old_agent.id}:{old_agent.full_name}"
        ),
        new_value=(
            f"{agent.id}:{agent.full_name}"
        ),
    )

    notify_user(
        db,
        user_id=agent.id,
        notification_type=(
            NotificationType.TICKET_REASSIGNED
        ),
        title="Ticket reassigned to you",
        message=(
            f"{ticket.ticket_number} "
            f"has been reassigned to you."
        ),
        ticket_id=ticket.id,
    )

    notify_user(
        db,
        user_id=old_agent.id,
        notification_type=(
            NotificationType.TICKET_REASSIGNED
        ),
        title="Ticket reassigned",
        message=(
            f"{ticket.ticket_number} "
            "has been reassigned to another agent."
        ),
        ticket_id=ticket.id,
    )

    return ticket

def find_best_replacement_agent(
    db: Session,
    *,
    current_agent_id: int,
) -> User | None:
    config = get_or_create_app_config(
        db
    )

    agents = db.scalars(
        select(User)
        .where(
            User.is_active.is_(True),
        )
        .order_by(
            User.id.asc()
        )
    ).all()

    eligible_agents: list[
        tuple[int, User]
    ] = []

    for candidate in agents:
        if (
            candidate.role.name
            != UserRole.AGENT.value
        ):
            continue

        if (
            candidate.id
            == current_agent_id
        ):
            continue

        active_count = (
            count_active_agent_tickets(
                db,
                agent_id=candidate.id,
            )
        )

        if (
            active_count
            >= config.max_active_tickets_per_agent
        ):
            continue

        eligible_agents.append(
            (
                active_count,
                candidate,
            )
        )

    if not eligible_agents:
        return None

    eligible_agents.sort(
        key=lambda item: (
            item[0],
            item[1].id,
        )
    )

    return eligible_agents[0][1]