from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.core.constants import TicketPriority


class SLAConfigResponse(BaseModel):
    id: int
    priority: TicketPriority
    resolution_minutes: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class SLAConfigUpdateRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    resolution_minutes: int = Field(
        ge=1,
        le=43200,
    )

    is_active: bool


class TicketSLAStatusResponse(BaseModel):
    ticket_id: int
    ticket_number: str
    priority: TicketPriority

    created_at: datetime
    sla_deadline: datetime

    is_breached: bool
    remaining_seconds: int
    elapsed_seconds: int
    total_sla_seconds: int

    percentage_consumed: float
    is_at_risk: bool

class EscalationScanResponse(BaseModel):
    escalated_count: int
    ticket_ids: list[int]
    ticket_numbers: list[str]