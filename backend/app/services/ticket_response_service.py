from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants import (
    AuditEventType,
    NotificationType,
    TicketStatus,
    UserRole,
)
from app.models.ticket import Ticket
from app.models.ticket_response import TicketResponse
from app.models.user import User
from app.repositories.ticket_repository import (
    create_ticket_response,
    list_ticket_responses,
    save_ticket,
)
from app.schemas.ticket_response import (
    TicketConversationResponse,
    TicketResponseCreateRequest,
    TicketResponseItem,
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


def build_ticket_response_item(
    response: TicketResponse,
) -> TicketResponseItem:
    return TicketResponseItem(
        id=response.id,
        ticket_id=response.ticket_id,
        author_id=response.author_id,
        author_name=response.author.full_name,
        author_role=response.author.role.name,
        message=response.message,
        is_internal=response.is_internal,
        created_at=response.created_at,
        updated_at=response.updated_at,
    )


def validate_response_access(
    *,
    ticket: Ticket,
    user: User,
) -> None:
    role = user.role.name

    if role == UserRole.ADMIN.value:
        return

    if role == UserRole.REQUESTER.value:
        if ticket.requester_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You do not have permission "
                    "to access this ticket conversation."
                ),
            )

        return

    if role == UserRole.AGENT.value:
        if ticket.assigned_agent_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "You do not have permission "
                    "to access this ticket conversation."
                ),
            )

        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this ticket.",
    )


def add_ticket_response(
    db: Session,
    *,
    ticket: Ticket,
    author: User,
    payload: TicketResponseCreateRequest,
) -> TicketResponse:
    validate_response_access(
        ticket=ticket,
        user=author,
    )

    if ticket.status == TicketStatus.CLOSED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Closed tickets cannot receive new responses.",
        )

    role = author.role.name

    if (
        role == UserRole.ADMIN.value
        and not payload.is_internal
    ):
        config = get_or_create_app_config(
            db
        )

        if not config.allow_admin_public_response:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Administrator public responses "
                    "are currently disabled."
                ),
            )

    if (
        role == UserRole.REQUESTER.value
        and payload.is_internal
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requesters cannot create internal notes.",
        )

    if (
        role == UserRole.AGENT.value
        and ticket.assigned_agent_id != author.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the assigned agent can respond to this ticket.",
        )

    response = TicketResponse(
        ticket_id=ticket.id,
        author_id=author.id,
        message=payload.message,
        is_internal=payload.is_internal,
    )

    response = create_ticket_response(
        db,
        response,
    )

    if payload.is_internal:
        event_type = (
            AuditEventType.INTERNAL_NOTE_ADDED
        )

        description = (
            f"Internal note added by "
            f"{author.full_name}."
        )

    else:
        event_type = (
            AuditEventType.RESPONSE_ADDED
        )

        description = (
            f"Response added by "
            f"{author.full_name}."
        )


    record_audit_event(
        db,
        ticket=ticket,
        actor=author,
        event_type=event_type,
        description=description,
        new_value=str(response.id),
        is_internal=payload.is_internal,
    )
    if not payload.is_internal:
        if role == UserRole.AGENT.value:
            notify_user(
                db,
                user_id=ticket.requester_id,
                notification_type=(
                    NotificationType.TICKET_RESPONSE
                ),
                title="New response on your ticket",
                message=(
                    f"{ticket.ticket_number} "
                    "has a new support response."
                ),
                ticket_id=ticket.id,
            )

        elif role == UserRole.REQUESTER.value:
            if ticket.assigned_agent_id is not None:
                notify_user(
                    db,
                    user_id=ticket.assigned_agent_id,
                    notification_type=(
                        NotificationType.TICKET_RESPONSE
                    ),
                    title="Requester replied",
                    message=(
                        f"The requester replied to "
                        f"{ticket.ticket_number}."
                    ),
                    ticket_id=ticket.id,
                )
        elif role == UserRole.ADMIN.value:
            notify_user(
                db,
                user_id=ticket.requester_id,
                notification_type=(
                    NotificationType.TICKET_RESPONSE
                ),
                title="New response on your ticket",
                message=(
                    f"{ticket.ticket_number} "
                    "has a new supervisor response."
                ),
                ticket_id=ticket.id,
            )

    if (
        role == UserRole.AGENT.value
        and not payload.is_internal
        and ticket.first_response_at is None
    ):
        ticket.first_response_at = utc_now()

        save_ticket(
            db,
            ticket,
        )

    return response


def get_ticket_conversation(
    db: Session,
    *,
    ticket: Ticket,
    user: User,
) -> TicketConversationResponse:
    validate_response_access(
        ticket=ticket,
        user=user,
    )

    include_internal = (
        user.role.name
        in {
            UserRole.AGENT.value,
            UserRole.ADMIN.value,
        }
    )

    responses = list_ticket_responses(
        db,
        ticket_id=ticket.id,
        include_internal=include_internal,
    )

    return TicketConversationResponse(
        items=[
            build_ticket_response_item(response)
            for response in responses
        ],
        total=len(responses),
    )