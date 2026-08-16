from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.permissions import require_admin
from app.core.constants import UserRole
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repository import (
    list_active_agents,
)
from app.schemas.user import (
    AdminCreateUserRequest,
    UpdateUserRoleRequest,
    UpdateUserStatusRequest,
    UserListResponse,
    UserResponse,
)
from app.services.user_service import (
    admin_create_user,
    build_user_response,
    get_user_or_404,
    get_users,
    update_user_role,
    update_user_status,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=UserListResponse,
)
def list_all_users(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_admin: Annotated[
        User,
        Depends(require_admin),
    ],
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    search: str | None = Query(
        default=None,
        max_length=120,
    ),
    role: UserRole | None = Query(
        default=None,
    ),
    is_active: bool | None = Query(
        default=None,
    ),
):
    del current_admin

    return get_users(
        db,
        page=page,
        page_size=page_size,
        search=search,
        role=role,
        is_active=is_active,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    del current_admin

    user = get_user_or_404(
        db,
        user_id,
    )

    return build_user_response(
        user,
    )

@router.get(
    "/agents/eligible",
    response_model=list[UserResponse],
)
def get_eligible_agents(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    del current_admin

    agents = list_active_agents(
        db
    )

    return [
        build_user_response(agent)
        for agent in agents
    ]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_by_admin(
    payload: AdminCreateUserRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    del current_admin

    user = admin_create_user(
        db,
        payload,
    )

    return build_user_response(
        user,
    )


@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
)
def change_user_status(
    user_id: int,
    payload: UpdateUserStatusRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    user = get_user_or_404(
        db,
        user_id,
    )

    user = update_user_status(
        db,
        target_user=user,
        is_active=payload.is_active,
        acting_admin=current_admin,
    )

    return build_user_response(
        user,
    )


@router.patch(
    "/{user_id}/role",
    response_model=UserResponse,
)
def change_user_role(
    user_id: int,
    payload: UpdateUserRoleRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    current_admin: Annotated[
        User,
        Depends(require_admin),
    ],
):
    user = get_user_or_404(
        db,
        user_id,
    )

    user = update_user_role(
        db,
        target_user=user,
        new_role=payload.role,
        acting_admin=current_admin,
    )

    return build_user_response(
        user,
    )

