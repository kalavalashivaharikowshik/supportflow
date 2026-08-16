import asyncio

import jwt
from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.models.notification import Notification
from app.models.user import User
from app.repositories.user_repository import (
    get_user_by_id,
)
from app.websocket.manager import manager


def authenticate_websocket_user(
    db: Session,
    token: str,
) -> User | None:
    try:
        payload = decode_access_token(
            token
        )

        subject = payload.get("sub")

        if subject is None:
            return None

        user_id = int(subject)

    except (
        jwt.InvalidTokenError,
        ValueError,
    ):
        return None

    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        return None

    if not user.is_active:
        return None

    return user


async def close_unauthorized_websocket(
    websocket: WebSocket,
) -> None:
    await websocket.close(
        code=1008,
        reason="Authentication failed.",
    )


def build_notification_payload(
    notification: Notification,
) -> dict:
    return {
        "type": "NOTIFICATION",
        "data": {
            "id": notification.id,
            "user_id": notification.user_id,
            "ticket_id": notification.ticket_id,
            "notification_type": notification.type,
            "title": notification.title,
            "message": notification.message,
            "is_read": notification.is_read,
            "read_at": (
                notification.read_at.isoformat()
                if notification.read_at
                else None
            ),
            "created_at": (
                notification.created_at.isoformat()
            ),
        },
    }


async def push_notification(
    notification: Notification,
) -> None:
    await manager.send_to_user(
        notification.user_id,
        build_notification_payload(
            notification
        ),
    )


def push_notification_sync(
    notification: Notification,
) -> None:
    target_loop = manager.event_loop

    if (
        target_loop is None
        or not target_loop.is_running()
    ):
        return

    try:
        current_loop = (
            asyncio.get_running_loop()
        )

    except RuntimeError:
        current_loop = None

    if current_loop is target_loop:
        target_loop.create_task(
            push_notification(
                notification
            )
        )

    else:
        asyncio.run_coroutine_threadsafe(
            push_notification(
                notification
            ),
            target_loop,
        )