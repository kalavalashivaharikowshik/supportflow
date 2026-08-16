from datetime import datetime

from pydantic import BaseModel

from app.core.constants import NotificationType


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    ticket_id: int | None

    type: NotificationType

    title: str
    message: str

    is_read: bool
    read_at: datetime | None
    created_at: datetime


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]

    page: int
    page_size: int

    total: int
    total_pages: int


class NotificationUnreadCountResponse(BaseModel):
    unread_count: int


class MarkAllReadResponse(BaseModel):
    updated_count: int