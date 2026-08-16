import math

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants import NotificationType
from app.models.notification import Notification
from app.models.user import User
from app.repositories.notification_repository import (
    count_unread_notifications,
    create_notification,
    get_notification_by_id,
    list_user_notifications,
    mark_all_notifications_read,
    save_notification,
)
from app.schemas.notification import (
    NotificationListResponse,
    NotificationResponse,
)
from app.services.app_config_service import (
    get_or_create_app_config,
)
from app.services.websocket_service import (
    push_notification_sync,
)
from app.utils.datetime import utc_now


def build_notification_response(
    notification: Notification,
) -> NotificationResponse:
    return NotificationResponse(
        id=notification.id,
        user_id=notification.user_id,
        ticket_id=notification.ticket_id,
        type=NotificationType(
            notification.type
        ),
        title=notification.title,
        message=notification.message,
        is_read=notification.is_read,
        read_at=notification.read_at,
        created_at=notification.created_at,
    )


def notify_user(
    db: Session,
    *,
    user_id: int,
    notification_type: NotificationType,
    title: str,
    message: str,
    ticket_id: int | None = None,
) -> Notification | None:
    config = get_or_create_app_config(
        db
    )

    if not config.notifications_enabled:
        return None
    notification = Notification(
        user_id=user_id,
        ticket_id=ticket_id,
        type=notification_type.value,
        title=title,
        message=message,
        is_read=False,
    )

    notification = create_notification(
        db,
        notification,
    )

    if config.websocket_notifications_enabled:
        push_notification_sync(
            notification
        )

    return notification


def get_notifications(
    db: Session,
    *,
    user: User,
    page: int,
    page_size: int,
    unread_only: bool,
) -> NotificationListResponse:
    offset = (
        page - 1
    ) * page_size

    notifications, total = (
        list_user_notifications(
            db,
            user_id=user.id,
            unread_only=unread_only,
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

    return NotificationListResponse(
        items=[
            build_notification_response(
                notification
            )
            for notification
            in notifications
        ],
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )


def get_unread_count(
    db: Session,
    *,
    user: User,
) -> int:
    return count_unread_notifications(
        db,
        user_id=user.id,
    )


def mark_notification_read(
    db: Session,
    *,
    user: User,
    notification_id: int,
) -> Notification:
    notification = (
        get_notification_by_id(
            db,
            notification_id,
        )
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    if notification.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You do not have permission "
                "to access this notification."
            ),
        )

    if notification.is_read:
        return notification

    notification.is_read = True
    notification.read_at = utc_now()

    return save_notification(
        db,
        notification,
    )


def mark_all_read(
    db: Session,
    *,
    user: User,
) -> int:
    return mark_all_notifications_read(
        db,
        user_id=user.id,
        read_at=utc_now(),
    )