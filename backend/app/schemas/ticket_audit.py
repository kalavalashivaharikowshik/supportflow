from datetime import datetime

from pydantic import BaseModel

from app.core.constants import AuditEventType


class TicketAuditItem(BaseModel):
    id: int
    ticket_id: int

    actor_id: int | None
    actor_name: str
    actor_role: str | None

    event_type: AuditEventType

    old_value: str | None
    new_value: str | None

    description: str
    is_internal: bool

    created_at: datetime


class TicketAuditTimelineResponse(BaseModel):
    items: list[TicketAuditItem]
    total: int