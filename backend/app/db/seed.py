from sqlalchemy import select

from app.core.constants import UserRole
from app.db.database import SessionLocal
from app.models.app_config import AppConfig
from app.models.role import Role
from app.models.sla_config import SLAConfig

DEFAULT_ROLES = [
    UserRole.REQUESTER,
    UserRole.AGENT,
    UserRole.ADMIN,
]

DEFAULT_SLA_CONFIGS = {
    "LOW": 72 * 60,
    "MEDIUM": 24 * 60,
    "HIGH": 8 * 60,
    "CRITICAL": 2 * 60,
}

def seed_roles() -> None:
    db = SessionLocal()

    try:
        existing_roles = set(
            db.scalars(
                select(Role.name)
            ).all()
        )

        for role in DEFAULT_ROLES:
            if role.value not in existing_roles:
                db.add(
                    Role(
                        name=role.value,
                    )
                )

        db.commit()

    finally:
        db.close()

def seed_sla_configs() -> None:
    db = SessionLocal()

    try:
        existing_priorities = set(
            db.scalars(
                select(SLAConfig.priority)
            ).all()
        )

        for priority, minutes in DEFAULT_SLA_CONFIGS.items():
            if priority not in existing_priorities:
                db.add(
                    SLAConfig(
                        priority=priority,
                        resolution_minutes=minutes,
                        is_active=True,
                    )
                )

        db.commit()

    finally:
        db.close()

def seed_app_config() -> None:
    db = SessionLocal()

    try:
        existing = db.scalar(
            select(AppConfig)
            .limit(1)
        )

        if existing is None:
            db.add(
                AppConfig(
                    sla_warning_threshold_percent=80,
                    escalation_check_interval_seconds=60,
                    max_active_tickets_per_agent=20,
                    allow_requester_reopen=True,
                    allow_admin_public_response=True,
                    notifications_enabled=True,
                    websocket_notifications_enabled=True,
                )
            )

            db.commit()

    finally:
        db.close()

if __name__ == "__main__":
    seed_roles()
    seed_sla_configs()
    seed_app_config()