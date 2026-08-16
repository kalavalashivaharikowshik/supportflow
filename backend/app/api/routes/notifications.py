from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_user,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.notification import (
    MarkAllReadResponse,
    NotificationListResponse,
    NotificationResponse,
    NotificationUnreadCountResponse,
)
from app.services.notification_service import (
    build_notification_response,
    get_notifications,
    get_unread_count,
    mark_all_read,
    mark_notification_read,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get(
    "",
    response_model=NotificationListResponse,
)
def list_notifications(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
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
    unread_only: bool = Query(
        default=False,
    ),
):
    return get_notifications(
        db,
        user=current_user,
        page=page,
        page_size=page_size,
        unread_only=unread_only,
    )


@router.get(
    "/unread-count",
    response_model=NotificationUnreadCountResponse,
)
def unread_count(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    count = get_unread_count(
        db,
        user=current_user,
    )

    return NotificationUnreadCountResponse(
        unread_count=count,
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_read(
    notification_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    notification = mark_notification_read(
        db,
        user=current_user,
        notification_id=notification_id,
    )

    return build_notification_response(
        notification
    )


@router.patch(
    "/read-all",
    response_model=MarkAllReadResponse,
)
def mark_everything_read(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    updated_count = mark_all_read(
        db,
        user=current_user,
    )

    return MarkAllReadResponse(
        updated_count=updated_count,
    )