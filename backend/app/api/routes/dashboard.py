from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.permissions import (
    require_admin,
    require_agent,
    require_requester,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.dashboard import (
    AdminDashboardResponse,
    AgentDashboardResponse,
    RequesterDashboardResponse,
)
from app.services.dashboard_service import (
    get_admin_dashboard,
    get_agent_dashboard,
    get_requester_dashboard,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/requester",
    response_model=RequesterDashboardResponse,
)
def requester_dashboard(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    requester: Annotated[
        User,
        Depends(require_requester),
    ],
):
    return get_requester_dashboard(
        db,
        requester=requester,
    )


@router.get(
    "/agent",
    response_model=AgentDashboardResponse,
)
def agent_dashboard(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    agent: Annotated[
        User,
        Depends(require_agent),
    ],
):
    return get_agent_dashboard(
        db,
        agent=agent,
    )


@router.get(
    "/admin",
    response_model=AdminDashboardResponse,
)
def admin_dashboard(
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

    return get_admin_dashboard(
        db
    )