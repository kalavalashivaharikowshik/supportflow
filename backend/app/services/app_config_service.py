from sqlalchemy.orm import Session

from app.models.app_config import AppConfig
from app.repositories.app_config_repository import (
    get_app_config,
    save_app_config,
)
from app.schemas.app_config import (
    AppConfigResponse,
    AppConfigUpdateRequest,
)

DEFAULT_CONFIG = {
    "sla_warning_threshold_percent": 80,
    "escalation_check_interval_seconds": 60,
    "max_active_tickets_per_agent": 20,
    "auto_reassign_on_escalation": True,
    "allow_requester_reopen": True,
    "allow_admin_public_response": True,
    "notifications_enabled": True,
    "websocket_notifications_enabled": True,
}


def create_default_config(
    db: Session,
) -> AppConfig:
    config = AppConfig(
        **DEFAULT_CONFIG
    )

    return save_app_config(
        db,
        config,
    )


def get_or_create_app_config(
    db: Session,
) -> AppConfig:
    config = get_app_config(
        db
    )

    if config is None:
        config = create_default_config(
            db
        )

    return config


def build_app_config_response(
    config: AppConfig,
) -> AppConfigResponse:
    return AppConfigResponse(
        id=config.id,
        sla_warning_threshold_percent=(
            config.sla_warning_threshold_percent
        ),
        escalation_check_interval_seconds=(
            config.escalation_check_interval_seconds
        ),
        max_active_tickets_per_agent=(
            config.max_active_tickets_per_agent
        ),
        auto_reassign_on_escalation=(
            config.auto_reassign_on_escalation
        ),
        allow_requester_reopen=(
            config.allow_requester_reopen
        ),
        allow_admin_public_response=(
            config.allow_admin_public_response
        ),
        notifications_enabled=(
            config.notifications_enabled
        ),
        websocket_notifications_enabled=(
            config.websocket_notifications_enabled
        ),
        created_at=config.created_at,
        updated_at=config.updated_at,
    )


def update_app_config(
    db: Session,
    *,
    payload: AppConfigUpdateRequest,
) -> AppConfig:
    config = get_or_create_app_config(
        db
    )

    config.sla_warning_threshold_percent = (
        payload.sla_warning_threshold_percent
    )

    config.escalation_check_interval_seconds = (
        payload.escalation_check_interval_seconds
    )

    config.max_active_tickets_per_agent = (
        payload.max_active_tickets_per_agent
    )

    config.auto_reassign_on_escalation = (
        payload.auto_reassign_on_escalation
    )

    config.allow_requester_reopen = (
        payload.allow_requester_reopen
    )

    config.allow_admin_public_response = (
        payload.allow_admin_public_response
    )

    config.notifications_enabled = (
        payload.notifications_enabled
    )

    config.websocket_notifications_enabled = (
        payload.websocket_notifications_enabled
    )

    return save_app_config(
        db,
        config,
    )