from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class AppConfigResponse(BaseModel):
    id: int

    sla_warning_threshold_percent: int
    escalation_check_interval_seconds: int
    max_active_tickets_per_agent: int
    auto_reassign_on_escalation: bool

    allow_requester_reopen: bool
    allow_admin_public_response: bool

    notifications_enabled: bool
    websocket_notifications_enabled: bool

    created_at: datetime
    updated_at: datetime


class AppConfigUpdateRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    sla_warning_threshold_percent: int = Field(
        ge=50,
        le=99,
    )

    escalation_check_interval_seconds: int = Field(
        ge=10,
        le=3600,
    )

    max_active_tickets_per_agent: int = Field(
        ge=1,
        le=500,
    )
    auto_reassign_on_escalation: bool

    allow_requester_reopen: bool
    allow_admin_public_response: bool

    notifications_enabled: bool
    websocket_notifications_enabled: bool

    @model_validator(
        mode="after"
    )
    def validate_websocket_dependency(
        self,
    ):
        if (
            self.websocket_notifications_enabled
            and not self.notifications_enabled
        ):
            raise ValueError(
                "WebSocket notifications cannot be enabled "
                "when notifications are disabled."
            )

        return self