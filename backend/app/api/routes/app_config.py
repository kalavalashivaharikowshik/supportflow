from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.api.dependencies.permissions import (
    require_admin,
)
from app.db.database import get_db
from app.models.user import User
from app.scheduler.scheduler import (
    update_sla_job_interval,
)
from app.schemas.app_config import (
    AppConfigResponse,
    AppConfigUpdateRequest,
)
from app.services.app_config_service import (
    build_app_config_response,
    get_or_create_app_config,
    update_app_config,
)

router = APIRouter(
    prefix="/admin/config",
    tags=["Admin Configuration"],
)


@router.get(
    "",
    response_model=AppConfigResponse,
)
def get_configuration(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    del admin

    config = get_or_create_app_config(
        db
    )

    return build_app_config_response(
        config
    )


@router.put(
    "",
    response_model=AppConfigResponse,
)
def update_configuration(
    payload: AppConfigUpdateRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    del admin

    config = update_app_config(
        db,
        payload=payload,
    )

    update_sla_job_interval(
        config.escalation_check_interval_seconds
    )

    return build_app_config_response(
        config
    )