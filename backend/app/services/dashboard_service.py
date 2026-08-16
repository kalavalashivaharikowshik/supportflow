from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.constants import (
    TicketPriority,
    TicketStatus,
    UserRole,
)
from app.models.role import Role
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.dashboard import (
    AdminDashboardResponse,
    AgentDashboardResponse,
    AgentWorkloadItem,
    DashboardTicketItem,
    PriorityCount,
    RequesterDashboardResponse,
    StatusCount,
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

def build_dashboard_ticket_item(
    ticket: Ticket,
) -> DashboardTicketItem:
    return DashboardTicketItem(
        id=ticket.id,
        ticket_number=ticket.ticket_number,
        title=ticket.title,
        priority=ticket.priority,
        status=ticket.status,
        requester_id=ticket.requester_id,
        assigned_agent_id=(
            ticket.assigned_agent_id
        ),
        sla_deadline=ticket.sla_deadline,
        is_escalated=ticket.is_escalated,
        created_at=ticket.created_at,
    )

ACTIVE_TICKET_STATUSES = {
    TicketStatus.OPEN.value,
    TicketStatus.ASSIGNED.value,
    TicketStatus.IN_PROGRESS.value,
    TicketStatus.ESCALATED.value,
    TicketStatus.REOPENED.value,
}

def get_status_counts(
    db: Session,
    *,
    filters: list,
) -> list[StatusCount]:
    statement = (
        select(
            Ticket.status,
            func.count(Ticket.id),
        )
        .where(*filters)
        .group_by(Ticket.status)
    )

    rows = db.execute(
        statement
    ).all()

    count_map = {
        status: count
        for status, count in rows
    }

    return [
        StatusCount(
            status=status.value,
            count=count_map.get(
                status.value,
                0,
            ),
        )
        for status in TicketStatus
    ]

def get_priority_counts(
    db: Session,
    *,
    filters: list,
) -> list[PriorityCount]:
    statement = (
        select(
            Ticket.priority,
            func.count(Ticket.id),
        )
        .where(*filters)
        .group_by(Ticket.priority)
    )

    rows = db.execute(
        statement
    ).all()

    count_map = {
        priority: count
        for priority, count in rows
    }

    return [
        PriorityCount(
            priority=priority.value,
            count=count_map.get(
                priority.value,
                0,
            ),
        )
        for priority in TicketPriority
    ]

def count_tickets(
    db: Session,
    *,
    filters: list,
) -> int:
    statement = (
        select(
            func.count(Ticket.id)
        )
        .where(*filters)
    )

    return db.scalar(
        statement
    ) or 0

def get_recent_tickets(
    db: Session,
    *,
    filters: list,
    limit: int = 5,
) -> list[DashboardTicketItem]:
    statement = (
        select(Ticket)
        .where(*filters)
        .order_by(
            Ticket.created_at.desc()
        )
        .limit(limit)
    )

    tickets = list(
        db.scalars(statement).all()
    )

    return [
        build_dashboard_ticket_item(
            ticket
        )
        for ticket in tickets
    ]

def calculate_average_first_response_minutes(
    db: Session,
    *,
    filters: list,
) -> float | None:
    statement = (
        select(
            Ticket.created_at,
            Ticket.first_response_at,
        )
        .where(
            *filters,
            Ticket.first_response_at.is_not(None),
        )
    )

    rows = db.execute(
        statement
    ).all()

    if not rows:
        return None

    total_minutes = 0.0

    for created_at, first_response_at in rows:
        created = normalize_datetime(
            created_at
        )

        first_response = normalize_datetime(
            first_response_at
        )

        total_minutes += (
            first_response - created
        ).total_seconds() / 60

    return round(
        total_minutes / len(rows),
        2,
    )

def calculate_average_resolution_minutes(
    db: Session,
    *,
    filters: list,
) -> float | None:
    statement = (
        select(
            Ticket.created_at,
            Ticket.resolved_at,
        )
        .where(
            *filters,
            Ticket.resolved_at.is_not(None),
        )
    )

    rows = db.execute(
        statement
    ).all()

    if not rows:
        return None

    total_minutes = 0.0

    for created_at, resolved_at in rows:
        created = normalize_datetime(
            created_at
        )

        resolved = normalize_datetime(
            resolved_at
        )

        total_minutes += (
            resolved - created
        ).total_seconds() / 60

    return round(
        total_minutes / len(rows),
        2,
    )

def get_requester_dashboard(
    db: Session,
    *,
    requester: User,
) -> RequesterDashboardResponse:
    base_filters = [
        Ticket.requester_id
        == requester.id
    ]

    total_tickets = count_tickets(
        db,
        filters=base_filters,
    )

    open_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.status
            == TicketStatus.OPEN.value,
        ],
    )

    active_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.status.in_(
                ACTIVE_TICKET_STATUSES
            ),
        ],
    )

    resolved_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.status
            == TicketStatus.RESOLVED.value,
        ],
    )

    closed_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.status
            == TicketStatus.CLOSED.value,
        ],
    )

    escalated_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.is_escalated.is_(True),
        ],
    )

    sla_at_risk_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.sla_warning_sent.is_(True),
            Ticket.is_escalated.is_(False),
            Ticket.status.in_(
                ACTIVE_TICKET_STATUSES
            ),
        ],
    )

    return RequesterDashboardResponse(
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        active_tickets=active_tickets,
        resolved_tickets=resolved_tickets,
        closed_tickets=closed_tickets,
        escalated_tickets=escalated_tickets,
        sla_at_risk_tickets=(
            sla_at_risk_tickets
        ),
        status_counts=get_status_counts(
            db,
            filters=base_filters,
        ),
        priority_counts=get_priority_counts(
            db,
            filters=base_filters,
        ),
        recent_tickets=get_recent_tickets(
            db,
            filters=base_filters,
        ),
    )

def get_agent_dashboard(
    db: Session,
    *,
    agent: User,
) -> AgentDashboardResponse:
    base_filters = [
        Ticket.assigned_agent_id
        == agent.id
    ]

    total_assigned_tickets = count_tickets(
        db,
        filters=base_filters,
    )

    active_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.status.in_(
                ACTIVE_TICKET_STATUSES
            ),
        ],
    )

    assigned_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.status
            == TicketStatus.ASSIGNED.value,
        ],
    )

    in_progress_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.status
            == TicketStatus.IN_PROGRESS.value,
        ],
    )

    escalated_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.is_escalated.is_(True),
            Ticket.status
            != TicketStatus.CLOSED.value,
        ],
    )

    resolved_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.status
            == TicketStatus.RESOLVED.value,
        ],
    )

    sla_at_risk_tickets = count_tickets(
        db,
        filters=[
            *base_filters,
            Ticket.sla_warning_sent.is_(True),
            Ticket.is_escalated.is_(False),
            Ticket.status.in_(
                ACTIVE_TICKET_STATUSES
            ),
        ],
    )

    return AgentDashboardResponse(
        total_assigned_tickets=(
            total_assigned_tickets
        ),
        active_tickets=active_tickets,
        assigned_tickets=assigned_tickets,
        in_progress_tickets=(
            in_progress_tickets
        ),
        escalated_tickets=(
            escalated_tickets
        ),
        resolved_tickets=resolved_tickets,
        sla_at_risk_tickets=(
            sla_at_risk_tickets
        ),
        status_counts=get_status_counts(
            db,
            filters=base_filters,
        ),
        priority_counts=get_priority_counts(
            db,
            filters=base_filters,
        ),
        average_first_response_minutes=(
            calculate_average_first_response_minutes(
                db,
                filters=base_filters,
            )
        ),
        average_resolution_minutes=(
            calculate_average_resolution_minutes(
                db,
                filters=base_filters,
            )
        ),
        recent_tickets=get_recent_tickets(
            db,
            filters=base_filters,
        ),
    )

def get_agent_workload(
    db: Session,
) -> list[AgentWorkloadItem]:
    agents_statement = (
        select(User)
        .join(
            Role,
            User.role_id == Role.id,
        )
        .where(
            Role.name == UserRole.AGENT.value,
            User.is_active.is_(True),
        )
        .order_by(
            User.full_name.asc()
        )
    )

    agents = list(
        db.scalars(
            agents_statement
        ).all()
    )

    workload: list[
        AgentWorkloadItem
    ] = []

    for agent in agents:
        base_filters = [
            Ticket.assigned_agent_id
            == agent.id
        ]

        total_assigned = count_tickets(
            db,
            filters=base_filters,
        )

        active_tickets = count_tickets(
            db,
            filters=[
                *base_filters,
                Ticket.status.in_(
                    ACTIVE_TICKET_STATUSES
                ),
            ],
        )

        escalated_tickets = count_tickets(
            db,
            filters=[
                *base_filters,
                Ticket.is_escalated.is_(
                    True
                ),
                Ticket.status
                != TicketStatus.CLOSED.value,
            ],
        )

        workload.append(
            AgentWorkloadItem(
                agent_id=agent.id,
                full_name=agent.full_name,
                email=agent.email,
                total_assigned=(
                    total_assigned
                ),
                active_tickets=(
                    active_tickets
                ),
                escalated_tickets=(
                    escalated_tickets
                ),
            )
        )

    return workload

def count_users_by_role(
    db: Session,
    *,
    role_name: str,
    active_only: bool = False,
) -> int:
    filters = [
        Role.name == role_name,
    ]

    if active_only:
        filters.append(
            User.is_active.is_(True)
        )

    statement = (
        select(
            func.count(User.id)
        )
        .join(
            Role,
            User.role_id == Role.id,
        )
        .where(*filters)
    )

    return db.scalar(
        statement
    ) or 0

def get_recent_escalations(
    db: Session,
    *,
    limit: int = 5,
) -> list[DashboardTicketItem]:
    statement = (
        select(Ticket)
        .where(
            Ticket.is_escalated.is_(True)
        )
        .order_by(
            Ticket.escalated_at.desc()
        )
        .limit(limit)
    )

    tickets = list(
        db.scalars(
            statement
        ).all()
    )

    return [
        build_dashboard_ticket_item(
            ticket
        )
        for ticket in tickets
    ]

def get_admin_dashboard(
    db: Session,
) -> AdminDashboardResponse:
    total_tickets = count_tickets(
        db,
        filters=[],
    )

    open_tickets = count_tickets(
        db,
        filters=[
            Ticket.status
            == TicketStatus.OPEN.value,
        ],
    )

    active_tickets = count_tickets(
        db,
        filters=[
            Ticket.status.in_(
                ACTIVE_TICKET_STATUSES
            ),
        ],
    )

    resolved_tickets = count_tickets(
        db,
        filters=[
            Ticket.status
            == TicketStatus.RESOLVED.value,
        ],
    )

    closed_tickets = count_tickets(
        db,
        filters=[
            Ticket.status
            == TicketStatus.CLOSED.value,
        ],
    )

    unassigned_tickets = count_tickets(
        db,
        filters=[
            Ticket.assigned_agent_id.is_(
                None
            ),
            Ticket.status.in_(
                ACTIVE_TICKET_STATUSES
            ),
        ],
    )

    escalated_tickets = count_tickets(
        db,
        filters=[
            Ticket.is_escalated.is_(True),
            Ticket.status
            != TicketStatus.CLOSED.value,
        ],
    )

    sla_at_risk_tickets = count_tickets(
        db,
        filters=[
            Ticket.sla_warning_sent.is_(True),
            Ticket.is_escalated.is_(False),
            Ticket.status.in_(
                ACTIVE_TICKET_STATUSES
            ),
        ],
    )

    total_requesters = count_users_by_role(
        db,
        role_name=(
            UserRole.REQUESTER.value
        ),
    )

    total_agents = count_users_by_role(
        db,
        role_name=UserRole.AGENT.value,
    )

    active_agents = count_users_by_role(
        db,
        role_name=UserRole.AGENT.value,
        active_only=True,
    )

    return AdminDashboardResponse(
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        active_tickets=active_tickets,
        resolved_tickets=resolved_tickets,
        closed_tickets=closed_tickets,
        unassigned_tickets=(
            unassigned_tickets
        ),
        escalated_tickets=(
            escalated_tickets
        ),
        sla_at_risk_tickets=(
            sla_at_risk_tickets
        ),
        total_requesters=(
            total_requesters
        ),
        total_agents=total_agents,
        active_agents=active_agents,
        status_counts=get_status_counts(
            db,
            filters=[],
        ),
        priority_counts=get_priority_counts(
            db,
            filters=[],
        ),
        average_first_response_minutes=(
            calculate_average_first_response_minutes(
                db,
                filters=[],
            )
        ),
        average_resolution_minutes=(
            calculate_average_resolution_minutes(
                db,
                filters=[],
            )
        ),
        recent_tickets=get_recent_tickets(
            db,
            filters=[],
        ),
        recent_escalations=(
            get_recent_escalations(
                db
            )
        ),
        agent_workload=get_agent_workload(
            db
        ),
    )