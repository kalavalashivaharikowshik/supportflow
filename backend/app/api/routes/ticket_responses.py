from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_user,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.ticket_response import (
    TicketConversationResponse,
    TicketResponseCreateRequest,
    TicketResponseItem,
)
from app.services.ticket_response_service import (
    add_ticket_response,
    build_ticket_response_item,
    get_ticket_conversation,
)
from app.services.ticket_service import (
    get_admin_ticket,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Ticket Responses"],
)


@router.post(
    "/{ticket_id}/responses",
    response_model=TicketResponseItem,
    status_code=status.HTTP_201_CREATED,
)
def create_response(
    ticket_id: int,
    payload: TicketResponseCreateRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    ticket = get_admin_ticket(
        db,
        ticket_id=ticket_id,
    )

    response = add_ticket_response(
        db,
        ticket=ticket,
        author=current_user,
        payload=payload,
    )

    return build_ticket_response_item(
        response
    )


@router.get(
    "/{ticket_id}/responses",
    response_model=TicketConversationResponse,
)
def get_responses(
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
    ticket = get_admin_ticket(
        db,
        ticket_id=ticket_id,
    )

    return get_ticket_conversation(
        db,
        ticket=ticket,
        user=current_user,
    )