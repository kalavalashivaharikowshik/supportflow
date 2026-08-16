import csv
from datetime import datetime, timezone
from io import StringIO

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.constants import (
    TicketStatus,
    UserRole,
)
from app.models.role import Role
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.common import (
    AgentPerformanceReportItem,
    SLAReportItem,
    TicketReportSummary,
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

def build_date_filters(
    *,
    start_date: datetime | None,
    end_date: datetime | None,
) -> list:
    filters = []

    if start_date is not None:
        filters.append(
            Ticket.created_at >= start_date
        )

    if end_date is not None:
        filters.append(
            Ticket.created_at <= end_date
        )

    return filters

def get_ticket_report_summary(
    db: Session,
    *,
    start_date: datetime | None,
    end_date: datetime | None,
) -> TicketReportSummary:
    date_filters = build_date_filters(
        start_date=start_date,
        end_date=end_date,
    )

    total = db.scalar(
        select(
            func.count(Ticket.id)
        ).where(*date_filters)
    ) or 0

    active = db.scalar(
        select(
            func.count(Ticket.id)
        ).where(
            *date_filters,
            Ticket.status.in_(
                [
                    TicketStatus.OPEN.value,
                    TicketStatus.ASSIGNED.value,
                    TicketStatus.IN_PROGRESS.value,
                    TicketStatus.ESCALATED.value,
                    TicketStatus.REOPENED.value,
                ]
            ),
        )
    ) or 0

    resolved = db.scalar(
        select(
            func.count(Ticket.id)
        ).where(
            *date_filters,
            Ticket.status
            == TicketStatus.RESOLVED.value,
        )
    ) or 0

    closed = db.scalar(
        select(
            func.count(Ticket.id)
        ).where(
            *date_filters,
            Ticket.status
            == TicketStatus.CLOSED.value,
        )
    ) or 0

    escalated = db.scalar(
        select(
            func.count(Ticket.id)
        ).where(
            *date_filters,
            Ticket.is_escalated.is_(True),
        )
    ) or 0

    sla_breached = escalated

    return TicketReportSummary(
        total_tickets=total,
        active_tickets=active,
        resolved_tickets=resolved,
        closed_tickets=closed,
        escalated_tickets=escalated,
        sla_breached_tickets=sla_breached,
    )

def get_sla_breach_report(
    db: Session,
    *,
    start_date: datetime | None,
    end_date: datetime | None,
) -> list[SLAReportItem]:
    filters = [
        Ticket.is_escalated.is_(True),
    ]

    filters.extend(
        build_date_filters(
            start_date=start_date,
            end_date=end_date,
        )
    )

    statement = (
        select(Ticket)
        .where(*filters)
        .order_by(
            Ticket.escalated_at.desc()
        )
    )

    tickets = list(
        db.scalars(statement).all()
    )

    return [
        SLAReportItem(
            ticket_id=ticket.id,
            ticket_number=ticket.ticket_number,
            title=ticket.title,
            priority=ticket.priority,
            status=ticket.status,
            requester_id=ticket.requester_id,
            assigned_agent_id=(
                ticket.assigned_agent_id
            ),
            created_at=ticket.created_at,
            sla_deadline=ticket.sla_deadline,
            escalated_at=ticket.escalated_at,
            resolved_at=ticket.resolved_at,
            is_escalated=ticket.is_escalated,
        )
        for ticket in tickets
    ]

def calculate_agent_average_first_response(
    tickets: list[Ticket],
) -> float | None:
    durations: list[float] = []

    for ticket in tickets:
        if ticket.first_response_at is None:
            continue

        created_at = normalize_datetime(
            ticket.created_at
        )

        first_response_at = normalize_datetime(
            ticket.first_response_at
        )

        durations.append(
            (
                first_response_at
                - created_at
            ).total_seconds()
            / 60
        )

    if not durations:
        return None

    return round(
        sum(durations)
        / len(durations),
        2,
    )

def calculate_agent_average_resolution(
    tickets: list[Ticket],
) -> float | None:
    durations: list[float] = []

    for ticket in tickets:
        if ticket.resolved_at is None:
            continue

        created_at = normalize_datetime(
            ticket.created_at
        )

        resolved_at = normalize_datetime(
            ticket.resolved_at
        )

        durations.append(
            (
                resolved_at
                - created_at
            ).total_seconds()
            / 60
        )

    if not durations:
        return None

    return round(
        sum(durations)
        / len(durations),
        2,
    )

def get_agent_performance_report(
    db: Session,
    *,
    start_date: datetime | None,
    end_date: datetime | None,
) -> list[AgentPerformanceReportItem]:
    agents = list(
        db.scalars(
            select(User)
            .join(
                Role,
                User.role_id == Role.id,
            )
            .where(
                Role.name
                == UserRole.AGENT.value
            )
            .order_by(
                User.full_name.asc()
            )
        ).all()
    )

    result: list[
        AgentPerformanceReportItem
    ] = []

    date_filters = build_date_filters(
        start_date=start_date,
        end_date=end_date,
    )

    for agent in agents:
        tickets = list(
            db.scalars(
                select(Ticket)
                .where(
                    Ticket.assigned_agent_id
                    == agent.id,
                    *date_filters,
                )
            ).all()
        )

        total_assigned = len(tickets)

        active_tickets = sum(
            1
            for ticket in tickets
            if ticket.status
            in {
                TicketStatus.ASSIGNED.value,
                TicketStatus.IN_PROGRESS.value,
                TicketStatus.ESCALATED.value,
                TicketStatus.REOPENED.value,
            }
        )

        resolved_tickets = sum(
            1
            for ticket in tickets
            if ticket.status
            in {
                TicketStatus.RESOLVED.value,
                TicketStatus.CLOSED.value,
            }
        )

        escalated_tickets = sum(
            1
            for ticket in tickets
            if ticket.is_escalated
        )

        result.append(
            AgentPerformanceReportItem(
                agent_id=agent.id,
                full_name=agent.full_name,
                email=agent.email,
                total_assigned=total_assigned,
                active_tickets=active_tickets,
                resolved_tickets=resolved_tickets,
                escalated_tickets=(
                    escalated_tickets
                ),
                average_first_response_minutes=(
                    calculate_agent_average_first_response(
                        tickets
                    )
                ),
                average_resolution_minutes=(
                    calculate_agent_average_resolution(
                        tickets
                    )
                ),
            )
        )

    return result

def create_csv(
    *,
    headers: list[str],
    rows: list[list],
) -> str:
    buffer = StringIO()

    writer = csv.writer(
        buffer
    )

    writer.writerow(
        headers
    )

    writer.writerows(
        rows
    )

    return buffer.getvalue()

def export_ticket_report_csv(
    db: Session,
    *,
    start_date: datetime | None,
    end_date: datetime | None,
) -> str:
    filters = build_date_filters(
        start_date=start_date,
        end_date=end_date,
    )

    tickets = list(
        db.scalars(
            select(Ticket)
            .where(*filters)
            .order_by(
                Ticket.created_at.desc()
            )
        ).all()
    )

    rows = []

    for ticket in tickets:
        rows.append(
            [
                ticket.ticket_number,
                ticket.title,
                ticket.category,
                ticket.priority,
                ticket.status,
                ticket.requester_id,
                ticket.assigned_agent_id,
                ticket.created_at.isoformat(),
                ticket.sla_deadline.isoformat(),
                (
                    ticket.first_response_at.isoformat()
                    if ticket.first_response_at
                    else ""
                ),
                (
                    ticket.resolved_at.isoformat()
                    if ticket.resolved_at
                    else ""
                ),
                ticket.is_escalated,
                (
                    ticket.escalated_at.isoformat()
                    if ticket.escalated_at
                    else ""
                ),
            ]
        )

    return create_csv(
        headers=[
            "ticket_number",
            "title",
            "category",
            "priority",
            "status",
            "requester_id",
            "assigned_agent_id",
            "created_at",
            "sla_deadline",
            "first_response_at",
            "resolved_at",
            "is_escalated",
            "escalated_at",
        ],
        rows=rows,
    )

def export_sla_report_csv(
    db: Session,
    *,
    start_date: datetime | None,
    end_date: datetime | None,
) -> str:
    items = get_sla_breach_report(
        db,
        start_date=start_date,
        end_date=end_date,
    )

    rows = [
        [
            item.ticket_number,
            item.title,
            item.priority,
            item.status,
            item.requester_id,
            item.assigned_agent_id,
            item.created_at.isoformat(),
            item.sla_deadline.isoformat(),
            (
                item.escalated_at.isoformat()
                if item.escalated_at
                else ""
            ),
            (
                item.resolved_at.isoformat()
                if item.resolved_at
                else ""
            ),
        ]
        for item in items
    ]

    return create_csv(
        headers=[
            "ticket_number",
            "title",
            "priority",
            "status",
            "requester_id",
            "assigned_agent_id",
            "created_at",
            "sla_deadline",
            "escalated_at",
            "resolved_at",
        ],
        rows=rows,
    )

def export_agent_performance_csv(
    db: Session,
    *,
    start_date: datetime | None,
    end_date: datetime | None,
) -> str:
    items = get_agent_performance_report(
        db,
        start_date=start_date,
        end_date=end_date,
    )

    rows = [
        [
            item.agent_id,
            item.full_name,
            item.email,
            item.total_assigned,
            item.active_tickets,
            item.resolved_tickets,
            item.escalated_tickets,
            (
                item.average_first_response_minutes
                if item.average_first_response_minutes
                is not None
                else ""
            ),
            (
                item.average_resolution_minutes
                if item.average_resolution_minutes
                is not None
                else ""
            ),
        ]
        for item in items
    ]

    return create_csv(
        headers=[
            "agent_id",
            "full_name",
            "email",
            "total_assigned",
            "active_tickets",
            "resolved_tickets",
            "escalated_tickets",
            "average_first_response_minutes",
            "average_resolution_minutes",
        ],
        rows=rows,
    )