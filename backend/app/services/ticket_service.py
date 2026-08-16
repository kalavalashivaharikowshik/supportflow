import math

from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.constants import (
    AuditEventType,
    SortDirection,
    TicketCategory,
    TicketPriority,
    TicketSortField,
    TicketStatus,
    UserRole,
)
from app.models.ticket import Ticket
from app.models.user import User
from app.repositories.ticket_repository import (
    create_ticket as create_ticket_record,
)
from app.repositories.ticket_repository import (
    get_ticket_by_id,
    list_agent_tickets,
    list_all_tickets,
    list_escalated_tickets,
    list_requester_tickets,
    save_ticket,
)
from app.schemas.ticket import (
    TicketCreateRequest,
    TicketListResponse,
    TicketResponse,
)
from app.services.audit_service import (
    record_audit_event,
)
from app.services.sla_service import (
    calculate_sla_deadline,
)
from app.utils.datetime import utc_now
from app.utils.ticket_number import (
    generate_ticket_number,
)


def build_ticket_response(
    ticket: Ticket,
) -> TicketResponse:
    return TicketResponse(
        id=ticket.id,
        ticket_number=ticket.ticket_number,
        title=ticket.title,
        description=ticket.description,
        category=TicketCategory(
            ticket.category
        ),
        priority=TicketPriority(
            ticket.priority
        ),
        status=TicketStatus(
            ticket.status
        ),
        requester_id=ticket.requester_id,
        assigned_agent_id=(
            ticket.assigned_agent_id
        ),
        assigned_at=ticket.assigned_at,
        assigned_by_id=ticket.assigned_by_id,
        sla_deadline=ticket.sla_deadline,
        sla_warning_sent=(
            ticket.sla_warning_sent
        ),
        first_response_at=(
            ticket.first_response_at
        ),
        resolved_at=ticket.resolved_at,
        closed_at=ticket.closed_at,
        is_escalated=(
            ticket.is_escalated
        ),
        escalated_at=(
            ticket.escalated_at
        ),
        resolution_summary=(
            ticket.resolution_summary
        ),
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
    )


def create_requester_ticket(
    db: Session,
    *,
    requester: User,
    payload: TicketCreateRequest,
) -> Ticket:
    created_at = utc_now()

    ticket = Ticket(
        title=payload.title,
        description=payload.description,
        category=payload.category.value,
        priority=payload.priority.value,
        status=TicketStatus.OPEN.value,
        requester_id=requester.id,
        assigned_agent_id=None,
        sla_deadline=(
            calculate_sla_deadline(
                db,
                priority=payload.priority,
                created_at=created_at,
            )
        ),
        created_at=created_at,
        updated_at=created_at,
    )

    create_ticket_record(
        db,
        ticket,
    )

    ticket.ticket_number = (
        generate_ticket_number(
            ticket.id
        )
    )

    ticket = save_ticket(
        db,
        ticket,
    )

    record_audit_event(
        db,
        ticket=ticket,
        actor=requester,
        event_type=(
            AuditEventType.TICKET_CREATED
        ),
        description=(
            f"Ticket {ticket.ticket_number} "
            "was created."
        ),
        new_value=TicketStatus.OPEN.value,
    )

    return ticket


def get_requester_ticket(
    db: Session,
    *,
    requester: User,
    ticket_id: int,
) -> Ticket:
    ticket = get_ticket_by_id(
        db,
        ticket_id,
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )

    if (
        ticket.requester_id
        != requester.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You do not have permission "
                "to view this ticket."
            ),
        )

    return ticket


def get_requester_tickets(
    db: Session,
    *,
    requester: User,
    page: int,
    page_size: int,
    search: str | None,
    priority: TicketPriority | None,
    status_filter: TicketStatus | None,
    category: TicketCategory | None,
    sort_by: TicketSortField,
    sort_direction: SortDirection,
) -> TicketListResponse:
    offset = (
        page - 1
    ) * page_size

    tickets, total = (
        list_requester_tickets(
            db,
            requester_id=requester.id,
            search=search,
            priority=(
                priority.value
                if priority
                else None
            ),
            status=(
                status_filter.value
                if status_filter
                else None
            ),
            category=(
                category.value
                if category
                else None
            ),
            sort_by=sort_by.value,
            sort_direction=sort_direction.value,
            offset=offset,
            limit=page_size,
        )
    )

    total_pages = (
        math.ceil(
            total / page_size
        )
        if total
        else 0
    )

    return TicketListResponse(
        items=[
            build_ticket_response(
                ticket
            )
            for ticket in tickets
        ],
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )


def get_admin_ticket(
    db: Session,
    *,
    ticket_id: int,
) -> Ticket:
    ticket = get_ticket_by_id(
        db,
        ticket_id,
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )

    return ticket

def get_all_tickets(
    db: Session,
    *,
    page: int,
    page_size: int,
    search: str | None,
    priority: TicketPriority | None,
    status_filter: TicketStatus | None,
    category: TicketCategory | None,
    assigned_agent_id: int | None,
    is_escalated: bool | None,
    is_assigned: bool | None,
    is_sla_breached: bool | None,
    is_at_risk: bool | None,
    sort_by: TicketSortField,
    sort_direction: SortDirection,
) -> TicketListResponse:
    offset = (
        page - 1
    ) * page_size

    tickets, total = list_all_tickets(
        db,
        search=search,
        priority=(
            priority.value
            if priority
            else None
        ),
        status=(
            status_filter.value
            if status_filter
            else None
        ),
        category=(
            category.value
            if category
            else None
        ),
        assigned_agent_id=assigned_agent_id,
        is_escalated=is_escalated,
        is_assigned=is_assigned,
        is_sla_breached=is_sla_breached,
        is_at_risk=is_at_risk,
        now=utc_now(),
        sort_by=sort_by.value,
        sort_direction=sort_direction.value,
        offset=offset,
        limit=page_size,
    )

    total_pages = (
        math.ceil(
            total / page_size
        )
        if total
        else 0
    )

    return TicketListResponse(
        items=[
            build_ticket_response(
                ticket
            )
            for ticket in tickets
        ],
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )

def get_agent_tickets(
    db: Session,
    *,
    agent: User,
    page: int,
    page_size: int,
    search: str | None,
    priority: TicketPriority | None,
    status_filter: TicketStatus | None,
    category: TicketCategory | None,
    sort_by: TicketSortField,
    sort_direction: SortDirection,
) -> TicketListResponse:
    offset = (
        page - 1
    ) * page_size

    tickets, total = list_agent_tickets(
        db,
        agent_id=agent.id,
        search=search,
        priority=(
            priority.value
            if priority
            else None
        ),
        status=(
            status_filter.value
            if status_filter
            else None
        ),
        category=(
            category.value
            if category
            else None
        ),
        sort_by=sort_by.value,
        sort_direction=sort_direction.value,
        offset=offset,
        limit=page_size,
    )

    total_pages = (
        math.ceil(
            total / page_size
        )
        if total
        else 0
    )

    return TicketListResponse(
        items=[
            build_ticket_response(
                ticket
            )
            for ticket in tickets
        ],
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )

def get_agent_ticket(
    db: Session,
    *,
    agent: User,
    ticket_id: int,
) -> Ticket:
    ticket = get_ticket_by_id(
        db,
        ticket_id,
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )

    if ticket.assigned_agent_id != agent.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You do not have permission "
                "to access this ticket."
            ),
        )

    return ticket

def get_accessible_ticket(
    db: Session,
    *,
    user: User,
    ticket_id: int,
) -> Ticket:
    ticket = get_ticket_by_id(
        db,
        ticket_id,
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found.",
        )

    role = user.role.name

    if role == UserRole.ADMIN.value:
        return ticket

    if (
        role == UserRole.REQUESTER.value
        and ticket.requester_id == user.id
    ):
        return ticket

    if (
        role == UserRole.AGENT.value
        and ticket.assigned_agent_id == user.id
    ):
        return ticket

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=(
            "You do not have permission "
            "to access this ticket."
        ),
    )

def update_ticket_priority(
    db: Session,
    *,
    ticket: Ticket,
    new_priority: TicketPriority,
    admin: User,
) -> Ticket:
    if ticket.status in {
        TicketStatus.RESOLVED.value,
        TicketStatus.CLOSED.value,
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Priority cannot be changed "
                "after a ticket is resolved or closed."
            ),
        )

    if ticket.priority == new_priority.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Ticket already has this priority."
            ),
        )
    old_priority = ticket.priority

    new_deadline = calculate_sla_deadline(
        db,
        priority=new_priority,
        created_at=ticket.created_at,
    )

    ticket.priority = new_priority.value
    ticket.sla_deadline = new_deadline
    ticket.sla_warning_sent = False

    ticket = save_ticket(
        db,
        ticket,
    )
    record_audit_event(
        db,
        ticket=ticket,
        event_type=(
            AuditEventType.PRIORITY_CHANGED
        ),
        actor=admin,
        description=(
            f"Ticket priority changed from "
            f"{old_priority} to "
            f"{new_priority.value}."
        ),
        old_value=old_priority,
        new_value=new_priority.value,
    )
    return ticket

def get_escalated_tickets(
    db: Session,
    *,
    page: int,
    page_size: int,
    search: str | None,
    priority: TicketPriority | None,
    assigned_agent_id: int | None,
    sort_by: TicketSortField,
    sort_direction: SortDirection,
) -> TicketListResponse:
    offset = (
        page - 1
    ) * page_size

    tickets, total = (
        list_escalated_tickets(
            db,
            search=search,
            priority=(
                priority.value
                if priority
                else None
            ),
            assigned_agent_id=(
                assigned_agent_id
            ),
            sort_by=sort_by.value,
            sort_direction=sort_direction.value,
            offset=offset,
            limit=page_size,
        )
    )

    total_pages = (
        math.ceil(
            total / page_size
        )
        if total
        else 0
    )

    return TicketListResponse(
        items=[
            build_ticket_response(
                ticket
            )
            for ticket in tickets
        ],
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )