from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_user,
)
from app.api.dependencies.permissions import (
    require_admin,
    require_agent,
    require_requester,
)
from app.core.constants import (
    SortDirection,
    TicketCategory,
    TicketPriority,
    TicketSortField,
    TicketStatus,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.sla import (
    TicketSLAStatusResponse,
)
from app.schemas.ticket import (
    TicketAssignRequest,
    TicketCreateRequest,
    TicketListResponse,
    TicketPriorityUpdateRequest,
    TicketResolveRequest,
    TicketResponse,
)
from app.services.assignment_service import (
    assign_ticket,
    get_eligible_agent,
    reassign_ticket,
)
from app.services.sla_service import (
    calculate_ticket_sla_status,
)
from app.services.status_service import (
    close_ticket,
    reopen_ticket,
    resolve_ticket,
    start_ticket_work,
)
from app.services.ticket_service import (
    build_ticket_response,
    create_requester_ticket,
    get_accessible_ticket,
    get_admin_ticket,
    get_agent_ticket,
    get_agent_tickets,
    get_all_tickets,
    get_escalated_tickets,
    get_requester_ticket,
    get_requester_tickets,
    update_ticket_priority,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    payload: TicketCreateRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    requester: Annotated[
        User,
        Depends(require_requester),
    ],
):
    ticket = create_requester_ticket(
        db,
        requester=requester,
        payload=payload,
    )

    return build_ticket_response(
        ticket
    )


@router.get(
    "/my",
    response_model=TicketListResponse,
)
def list_my_tickets(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    requester: Annotated[
        User,
        Depends(require_requester),
    ],
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
        max_length=150,
    ),
    priority: TicketPriority | None = Query(
        default=None,
    ),
    status_filter: TicketStatus | None = Query(
        default=None,
        alias="status",
    ),
    category: TicketCategory | None = Query(
        default=None,
    ),
    sort_by: TicketSortField = Query(
        default=TicketSortField.CREATED_AT,
    ),

    sort_direction: SortDirection = Query(
        default=SortDirection.DESC,
    ),
):
    return get_requester_tickets(
        db,
        requester=requester,
        page=page,
        page_size=page_size,
        search=search,
        priority=priority,
        status_filter=status_filter,
        category=category,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )

@router.get(
    "/admin/all",
    response_model=TicketListResponse,
)
def list_all_tickets_for_admin(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
        max_length=150,
    ),
    priority: TicketPriority | None = Query(
        default=None,
    ),
    status_filter: TicketStatus | None = Query(
        default=None,
        alias="status",
    ),
    category: TicketCategory | None = Query(
        default=None,
    ),
    assigned_agent_id: int | None = Query(
        default=None,
        gt=0,
    ),
    is_escalated: bool | None = Query(
        default=None,
    ),
    is_assigned: bool | None = Query(
        default=None,
    ),

    is_sla_breached: bool | None = Query(
        default=None,
    ),

    is_at_risk: bool | None = Query(
        default=None,
    ),

    sort_by: TicketSortField = Query(
        default=TicketSortField.CREATED_AT,
    ),

    sort_direction: SortDirection = Query(
        default=SortDirection.DESC,
    ),
):
    del admin

    return get_all_tickets(
        db,
        page=page,
        page_size=page_size,
        search=search,
        priority=priority,
        status_filter=status_filter,
        category=category,
        assigned_agent_id=assigned_agent_id,
        is_escalated=is_escalated,
        is_assigned=is_assigned,
        is_sla_breached=is_sla_breached,
        is_at_risk=is_at_risk,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )
@router.patch(
    "/assigned/{ticket_id}/start",
    response_model=TicketResponse,
)
def start_assigned_ticket(
    ticket_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    agent: Annotated[
        User,
        Depends(require_agent),
    ],
):
    ticket = get_agent_ticket(
        db,
        agent=agent,
        ticket_id=ticket_id,
    )

    ticket = start_ticket_work(
        db,
        ticket=ticket,
        agent=agent,
    )

    return build_ticket_response(
        ticket
    )

@router.patch(
    "/assigned/{ticket_id}/resolve",
    response_model=TicketResponse,
)
def resolve_assigned_ticket(
    ticket_id: int,
    payload: TicketResolveRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    agent: Annotated[
        User,
        Depends(require_agent),
    ],
):
    ticket = get_agent_ticket(
        db,
        agent=agent,
        ticket_id=ticket_id,
    )

    ticket = resolve_ticket(
        db,
        ticket=ticket,
        agent=agent,
        resolution_summary=(
            payload.resolution_summary
        ),
    )

    return build_ticket_response(
        ticket
    )

@router.patch(
    "/{ticket_id}/close",
    response_model=TicketResponse,
)
def close_requester_ticket(
    ticket_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    requester: Annotated[
        User,
        Depends(require_requester),
    ],
):
    ticket = get_requester_ticket(
        db,
        requester=requester,
        ticket_id=ticket_id,
    )

    ticket = close_ticket(
        db,
        ticket=ticket,
        requester=requester,
    )

    return build_ticket_response(
        ticket
    )
@router.patch(
    "/{ticket_id}/reopen",
    response_model=TicketResponse,
)
def reopen_requester_ticket(
    ticket_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    requester: Annotated[
        User,
        Depends(require_requester),
    ],
):
    ticket = get_requester_ticket(
        db,
        requester=requester,
        ticket_id=ticket_id,
    )

    ticket = reopen_ticket(
        db,
        ticket=ticket,
        requester=requester,
    )

    return build_ticket_response(
        ticket
    )
@router.get(
    "/admin/escalated",
    response_model=TicketListResponse,
)
def list_escalated_tickets_for_admin(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
        max_length=150,
    ),
    priority: TicketPriority | None = Query(
        default=None,
    ),
    assigned_agent_id: int | None = Query(
        default=None,
        gt=0,
    ),
    sort_by: TicketSortField = Query(
        default=TicketSortField.SLA_DEADLINE,
    ),

    sort_direction: SortDirection = Query(
        default=SortDirection.ASC,
    ),
):
    del admin

    return get_escalated_tickets(
        db,
        page=page,
        page_size=page_size,
        search=search,
        priority=priority,
        assigned_agent_id=assigned_agent_id,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )
@router.get(
    "/admin/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket_for_admin(
    ticket_id: int,
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

    ticket = get_admin_ticket(
        db,
        ticket_id=ticket_id,
    )

    return build_ticket_response(
        ticket
    )

@router.patch(
    "/admin/{ticket_id}/assign",
    response_model=TicketResponse,
)
def assign_ticket_to_agent(
    ticket_id: int,
    payload: TicketAssignRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    ticket = get_admin_ticket(
        db,
        ticket_id=ticket_id,
    )

    agent = get_eligible_agent(
        db,
        payload.agent_id,
    )

    ticket = assign_ticket(
        db,
        ticket=ticket,
        agent=agent,
        admin=admin,
    )

    return build_ticket_response(
        ticket
    )

@router.patch(
    "/admin/{ticket_id}/reassign",
    response_model=TicketResponse,
)
def reassign_ticket_to_agent(
    ticket_id: int,
    payload: TicketAssignRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    ticket = get_admin_ticket(
        db,
        ticket_id=ticket_id,
    )

    agent = get_eligible_agent(
        db,
        payload.agent_id,
    )

    ticket = reassign_ticket(
        db,
        ticket=ticket,
        agent=agent,
        admin=admin,
    )

    return build_ticket_response(
        ticket
    )

@router.get(
    "/assigned/me",
    response_model=TicketListResponse,
)
def list_my_assigned_tickets(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    agent: Annotated[
        User,
        Depends(require_agent),
    ],
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
        max_length=150,
    ),
    priority: TicketPriority | None = Query(
        default=None,
    ),
    status_filter: TicketStatus | None = Query(
        default=None,
        alias="status",
    ),
    category: TicketCategory | None = Query(
        default=None,
    ),
    sort_by: TicketSortField = Query(
        default=TicketSortField.SLA_DEADLINE,
    ),

    sort_direction: SortDirection = Query(
        default=SortDirection.ASC,
    ),
):
    return get_agent_tickets(
        db,
        agent=agent,
        page=page,
        page_size=page_size,
        search=search,
        priority=priority,
        status_filter=status_filter,
        category=category,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )

@router.get(
    "/assigned/{ticket_id}",
    response_model=TicketResponse,
)
def get_assigned_ticket(
    ticket_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    agent: Annotated[
        User,
        Depends(require_agent),
    ],
):
    ticket = get_agent_ticket(
        db,
        agent=agent,
        ticket_id=ticket_id,
    )

    return build_ticket_response(
        ticket
    )

@router.get(
    "/{ticket_id}/sla",
    response_model=TicketSLAStatusResponse,
)
def get_ticket_sla_status(
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

    return calculate_ticket_sla_status(
        ticket
    )

@router.patch(
    "/admin/{ticket_id}/priority",
    response_model=TicketResponse,
)
def change_ticket_priority(
    ticket_id: int,
    payload: TicketPriorityUpdateRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    ticket = get_admin_ticket(
        db,
        ticket_id=ticket_id,
    )

    ticket = update_ticket_priority(
        db,
        ticket=ticket,
        new_priority=payload.priority,
        admin=admin
    )

    return build_ticket_response(
        ticket
    )

@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(
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

    return build_ticket_response(
        ticket
    )