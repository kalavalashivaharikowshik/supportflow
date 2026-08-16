from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.app_config import AppConfig


def get_app_config(
    db: Session,
) -> AppConfig | None:
    return db.scalar(
        select(AppConfig)
        .order_by(AppConfig.id.asc())
        .limit(1)
    )


def save_app_config(
    db: Session,
    config: AppConfig,
) -> AppConfig:
    db.add(config)
    db.commit()
    db.refresh(config)

    return config