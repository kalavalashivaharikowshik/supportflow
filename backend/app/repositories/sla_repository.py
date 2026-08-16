from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.sla_config import SLAConfig


def get_sla_config_by_priority(
    db: Session,
    priority: str,
) -> SLAConfig | None:
    return db.scalar(
        select(SLAConfig).where(
            SLAConfig.priority == priority,
        )
    )


def list_sla_configs(
    db: Session,
) -> list[SLAConfig]:
    statement = select(
        SLAConfig
    ).order_by(
        SLAConfig.resolution_minutes.asc()
    )

    return list(
        db.scalars(statement).all()
    )


def save_sla_config(
    db: Session,
    config: SLAConfig,
) -> SLAConfig:
    db.add(config)
    db.commit()
    db.refresh(config)

    return config