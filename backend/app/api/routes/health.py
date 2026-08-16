from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import (
    check_database_connection,
    get_db,
)

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health_check():
    return {
        "status": "healthy",
        "service": "SupportFlow API",
        "timestamp": datetime.now(
            timezone.utc,
        ).isoformat(),
    }


@router.get("/database")
def database_health_check(
    db: Annotated[Session, Depends(get_db)],
):
    check_database_connection(db)

    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now(
            timezone.utc,
        ).isoformat(),
    }