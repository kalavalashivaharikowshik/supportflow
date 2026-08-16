from sqlalchemy import (
    func,
    select,
    update,
)
from sqlalchemy.orm import Session

from app.models.notification import Notification


def create_notification(
    db: Session,
    notification: Notification,
) -> Notification:
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def list_user_notifications(
    db: Session,
    *,
    user_id: int,
    unread_only: bool,
    offset: int,
    limit: int,
) -> tuple[list[Notification], int]:
    filters = [
        Notification.user_id == user_id
    ]

    if unread_only:
        filters.append(
            Notification.is_read.is_(False)
        )

    statement = (
        select(Notification)
        .where(*filters)
        .order_by(
            Notification.created_at.desc()
        )
        .offset(offset)
        .limit(limit)
    )

    count_statement = (
        select(
            func.count(Notification.id)
        )
        .where(*filters)
    )

    notifications = list(
        db.scalars(statement).all()
    )

    total = db.scalar(
        count_statement
    ) or 0

    return notifications, total


def get_notification_by_id(
    db: Session,
    notification_id: int,
) -> Notification | None:
    return db.scalar(
        select(Notification).where(
            Notification.id
            == notification_id,
        )
    )


def count_unread_notifications(
    db: Session,
    *,
    user_id: int,
) -> int:
    statement = (
        select(
            func.count(Notification.id)
        )
        .where(
            Notification.user_id
            == user_id,
            Notification.is_read.is_(False),
        )
    )

    return db.scalar(statement) or 0


def mark_all_notifications_read(
    db: Session,
    *,
    user_id: int,
    read_at,
) -> int:
    statement = (
        update(Notification)
        .where(
            Notification.user_id
            == user_id,
            Notification.is_read.is_(False),
        )
        .values(
            is_read=True,
            read_at=read_at,
        )
    )

    result = db.execute(statement)
    db.commit()

    return result.rowcount or 0


def save_notification(
    db: Session,
    notification: Notification,
) -> Notification:
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification