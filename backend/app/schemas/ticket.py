from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from app.core.constants import (
    TicketCategory,
    TicketPriority,
    TicketStatus,
)


class TicketCreateRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    title: str = Field(
        min_length=3,
        max_length=150,
    )

    description: str = Field(
        min_length=10,
        max_length=5000,
    )

    category: TicketCategory

    priority: TicketPriority

    @field_validator("title", "description")
    @classmethod
    def normalize_text(
        cls,
        value: str,
    ) -> str:
        normalized = value.strip()

        if not normalized:
            raise ValueError(
                "Value cannot be blank."
            )

        return normalized


class TicketResponse(BaseModel):
    id: int
    ticket_number: str
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus

    requester_id: int
    assigned_agent_id: int | None
    assigned_at: datetime | None
    assigned_by_id: int | None

    sla_deadline: datetime
    sla_warning_sent: bool

    first_response_at: datetime | None
    resolved_at: datetime | None
    closed_at: datetime | None

    is_escalated: bool
    escalated_at: datetime | None

    resolution_summary: str | None

    created_at: datetime
    updated_at: datetime


class TicketListResponse(BaseModel):
    items: list[TicketResponse]
    page: int
    page_size: int
    total: int
    total_pages: int

class TicketAssignRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    agent_id: int = Field(
        gt=0,
    )

class TicketStatusUpdateRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    status: TicketStatus

class TicketResolveRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    resolution_summary: str = Field(
        min_length=10,
        max_length=5000,
    )

    @field_validator("resolution_summary")
    @classmethod
    def validate_resolution_summary(
        cls,
        value: str,
    ) -> str:
        normalized = value.strip()

        if len(normalized) < 10:
            raise ValueError(
                "Resolution summary must contain at least 10 characters."
            )

        return normalized

class TicketPriorityUpdateRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    priority: TicketPriority