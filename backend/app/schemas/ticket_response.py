from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class TicketResponseCreateRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    message: str = Field(
        min_length=1,
        max_length=5000,
    )

    is_internal: bool = False

    @field_validator("message")
    @classmethod
    def validate_message(
        cls,
        value: str,
    ) -> str:
        normalized = value.strip()

        if not normalized:
            raise ValueError(
                "Response message cannot be blank."
            )

        return normalized


class TicketResponseItem(BaseModel):
    id: int
    ticket_id: int

    author_id: int
    author_name: str
    author_role: str

    message: str
    is_internal: bool

    created_at: datetime
    updated_at: datetime


class TicketConversationResponse(BaseModel):
    items: list[TicketResponseItem]
    total: int