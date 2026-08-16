from datetime import datetime

from sqlalchemy import (
    case,
    func,
    or_,
    select,
)
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.ticket_response import TicketResponse
from app.models.user import User


def priority_order_expression():
    return case(
        (Ticket.priority == "CRITICAL", 4),
        (Ticket.priority == "HIGH", 3),
        (Ticket.priority == "MEDIUM", 2),
        (Ticket.priority == "LOW", 1),
        else_=0,
    )


def build_ticket_order_by(
    *,
    sort_by: str,
    sort_direction: str,
):
    if sort_by == "created_at":
        column = Ticket.created_at

    elif sort_by == "updated_at":
        column = Ticket.updated_at

    elif sort_by == "sla_deadline":
        column = Ticket.sla_deadline

    elif sort_by == "ticket_number":
        column = Ticket.ticket_number

    elif sort_by == "status":
        column = Ticket.status

    elif sort_by == "priority":
        column = priority_order_expression()

    else:
        column = Ticket.created_at

    if sort_direction == "asc":
        return column.asc()

    return column.desc()


def create_ticket(
    db: Session,
    ticket: Ticket,
) -> Ticket:
    db.add(ticket)
    db.flush()

    return ticket


def save_ticket(
    db: Session,
    ticket: Ticket,
) -> Ticket:
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def get_ticket_by_id(
    db: Session,
    ticket_id: int,
) -> Ticket | None:
    return db.scalar(
        select(Ticket).where(
            Ticket.id == ticket_id,
        )
    )


def get_ticket_by_number(
    db: Session,
    ticket_number: str,
) -> Ticket | None:
    return db.scalar(
        select(Ticket).where(
            Ticket.ticket_number == ticket_number,
        )
    )


def list_requester_tickets(
    db: Session,
    *,
    requester_id: int,
    search: str | None,
    priority: str | None,
    status: str | None,
    category: str | None,
    sort_by: str,
    sort_direction: str,
    offset: int,
    limit: int,
) -> tuple[list[Ticket], int]:
    filters = [
        Ticket.requester_id == requester_id,
    ]

    if search:
        pattern = f"%{search.strip()}%"

        filters.append(
            or_(
                Ticket.ticket_number.ilike(
                    pattern
                ),
                Ticket.title.ilike(
                    pattern
                ),
            )
        )

    if priority:
        filters.append(
            Ticket.priority == priority
        )

    if status:
        filters.append(
            Ticket.status == status
        )

    if category:
        filters.append(
            Ticket.category == category
        )

    statement = (
        select(Ticket)
        .where(*filters)
        .order_by(
            build_ticket_order_by(
                sort_by=sort_by,
                sort_direction=sort_direction,
            )
        )
        .offset(offset)
        .limit(limit)
    )

    count_statement = (
        select(
            func.count(Ticket.id)
        )
        .where(*filters)
    )

    tickets = list(
        db.scalars(statement).all()
    )

    total = (
        db.scalar(count_statement)
        or 0
    )

    return tickets, total


def list_all_tickets(
    db: Session,
    *,
    search: str | None,
    priority: str | None,
    status: str | None,
    category: str | None,
    assigned_agent_id: int | None,
    is_escalated: bool | None,
    is_assigned: bool | None,
    is_sla_breached: bool | None,
    is_at_risk: bool | None,
    now: datetime,
    sort_by: str,
    sort_direction: str,
    offset: int,
    limit: int,
) -> tuple[list[Ticket], int]:
    filters = []

    if search:
        pattern = f"%{search.strip()}%"

        filters.append(
            or_(
                Ticket.ticket_number.ilike(
                    pattern
                ),
                Ticket.title.ilike(
                    pattern
                ),
                User.full_name.ilike(
                    pattern
                ),
                User.email.ilike(
                    pattern
                ),
            )
        )

    if priority:
        filters.append(
            Ticket.priority == priority
        )

    if status:
        filters.append(
            Ticket.status == status
        )

    if category:
        filters.append(
            Ticket.category == category
        )

    if assigned_agent_id is not None:
        filters.append(
            Ticket.assigned_agent_id
            == assigned_agent_id
        )

    if is_escalated is not None:
        filters.append(
            Ticket.is_escalated
            == is_escalated
        )

    if is_assigned is True:
        filters.append(
            Ticket.assigned_agent_id.is_not(
                None
            )
        )

    elif is_assigned is False:
        filters.append(
            Ticket.assigned_agent_id.is_(
                None
            )
        )

    if is_sla_breached is True:
        filters.extend(
            [
                Ticket.sla_deadline <= now,
                Ticket.status.notin_(
                    [
                        "RESOLVED",
                        "CLOSED",
                    ]
                ),
            ]
        )

    elif is_sla_breached is False:
        filters.append(
            Ticket.sla_deadline > now
        )

    if is_at_risk is True:
        filters.extend(
            [
                Ticket.sla_warning_sent.is_(
                    True
                ),
                Ticket.is_escalated.is_(
                    False
                ),
                Ticket.status.notin_(
                    [
                        "RESOLVED",
                        "CLOSED",
                    ]
                ),
            ]
        )

    elif is_at_risk is False:
        filters.append(
            Ticket.sla_warning_sent.is_(
                False
            )
        )

    statement = (
        select(Ticket)
        .join(
            User,
            Ticket.requester_id == User.id,
        )
        .where(*filters)
        .order_by(
            build_ticket_order_by(
                sort_by=sort_by,
                sort_direction=sort_direction,
            )
        )
        .offset(offset)
        .limit(limit)
    )

    count_statement = (
        select(
            func.count(Ticket.id)
        )
        .join(
            User,
            Ticket.requester_id == User.id,
        )
        .where(*filters)
    )

    tickets = list(
        db.scalars(statement).all()
    )

    total = (
        db.scalar(count_statement)
        or 0
    )

    return tickets, total


def list_agent_tickets(
    db: Session,
    *,
    agent_id: int,
    search: str | None,
    priority: str | None,
    status: str | None,
    category: str | None,
    sort_by: str,
    sort_direction: str,
    offset: int,
    limit: int,
) -> tuple[list[Ticket], int]:
    filters = [
        Ticket.assigned_agent_id == agent_id,
    ]

    if search:
        pattern = f"%{search.strip()}%"

        filters.append(
            or_(
                Ticket.ticket_number.ilike(
                    pattern
                ),
                Ticket.title.ilike(
                    pattern
                ),
            )
        )

    if priority:
        filters.append(
            Ticket.priority == priority
        )

    if status:
        filters.append(
            Ticket.status == status
        )

    if category:
        filters.append(
            Ticket.category == category
        )

    statement = (
        select(Ticket)
        .where(*filters)
        .order_by(
            build_ticket_order_by(
                sort_by=sort_by,
                sort_direction=sort_direction,
            )
        )
        .offset(offset)
        .limit(limit)
    )

    count_statement = (
        select(
            func.count(Ticket.id)
        )
        .where(*filters)
    )

    tickets = list(
        db.scalars(statement).all()
    )

    total = (
        db.scalar(count_statement)
        or 0
    )

    return tickets, total


def create_ticket_response(
    db: Session,
    response: TicketResponse,
) -> TicketResponse:
    db.add(response)
    db.commit()
    db.refresh(response)

    return response


def list_ticket_responses(
    db: Session,
    *,
    ticket_id: int,
    include_internal: bool,
) -> list[TicketResponse]:
    filters = [
        TicketResponse.ticket_id
        == ticket_id,
    ]

    if not include_internal:
        filters.append(
            TicketResponse.is_internal.is_(
                False
            )
        )

    statement = (
        select(TicketResponse)
        .where(*filters)
        .order_by(
            TicketResponse.created_at.asc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def list_escalation_candidates(
    db: Session,
    *,
    now: datetime,
) -> list[Ticket]:
    eligible_statuses = [
        "OPEN",
        "ASSIGNED",
        "IN_PROGRESS",
        "REOPENED",
    ]

    statement = (
        select(Ticket)
        .where(
            Ticket.sla_deadline <= now,
            Ticket.is_escalated.is_(
                False
            ),
            Ticket.status.in_(
                eligible_statuses
            ),
        )
        .order_by(
            Ticket.sla_deadline.asc()
        )
    )

    return list(
        db.scalars(statement).all()
    )


def list_escalated_tickets(
    db: Session,
    *,
    search: str | None,
    priority: str | None,
    assigned_agent_id: int | None,
    sort_by: str,
    sort_direction: str,
    offset: int,
    limit: int,
) -> tuple[list[Ticket], int]:
    filters = [
        Ticket.is_escalated.is_(True),
    ]

    if search:
        pattern = f"%{search.strip()}%"

        filters.append(
            or_(
                Ticket.ticket_number.ilike(
                    pattern
                ),
                Ticket.title.ilike(
                    pattern
                ),
            )
        )

    if priority:
        filters.append(
            Ticket.priority == priority
        )

    if assigned_agent_id is not None:
        filters.append(
            Ticket.assigned_agent_id
            == assigned_agent_id
        )

    statement = (
        select(Ticket)
        .where(*filters)
        .order_by(
            build_ticket_order_by(
                sort_by=sort_by,
                sort_direction=sort_direction,
            )
        )
        .offset(offset)
        .limit(limit)
    )

    count_statement = (
        select(
            func.count(Ticket.id)
        )
        .where(*filters)
    )

    tickets = list(
        db.scalars(statement).all()
    )

    total = (
        db.scalar(count_statement)
        or 0
    )

    return tickets, total


def list_sla_warning_candidates(
    db: Session,
    *,
    now: datetime,
) -> list[Ticket]:
    eligible_statuses = [
        "OPEN",
        "ASSIGNED",
        "IN_PROGRESS",
        "REOPENED",
    ]

    statement = (
        select(Ticket)
        .where(
            Ticket.sla_warning_sent.is_(
                False
            ),
            Ticket.is_escalated.is_(
                False
            ),
            Ticket.sla_deadline > now,
            Ticket.status.in_(
                eligible_statuses
            ),
        )
    )

    return list(
        db.scalars(statement).all()
    )

def count_active_agent_tickets(
        db: Session,
        *,
        agent_id: int,
    ) -> int:
        active_statuses = [
            "ASSIGNED",
            "IN_PROGRESS",
            "ESCALATED",
            "REOPENED",
        ]

        statement = (
            select(
                func.count(Ticket.id)
            )
            .where(
                Ticket.assigned_agent_id
                == agent_id,
                Ticket.status.in_(
                    active_statuses
                ),
            )
        )

        return db.scalar(
            statement
        ) or 0