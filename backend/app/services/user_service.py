import math

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants import UserRole
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_role_by_name,
    get_user_by_email,
    get_user_by_id,
    list_users,
    save_user,
)
from app.schemas.user import (
    AdminCreateUserRequest,
    UpdateProfileRequest,
    UserListResponse,
    UserResponse,
)


def update_profile(
    db: Session,
    user: User,
    payload: UpdateProfileRequest,
) -> User:
    normalized_email = (
        str(payload.email)
        .strip()
        .lower()
    )

    existing_user = get_user_by_email(
        db,
        normalized_email,
    )

    if (
        existing_user is not None
        and existing_user.id != user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user.full_name = payload.full_name
    user.email = normalized_email

    return save_user(
        db,
        user,
    )

def build_user_response(
    user: User,
) -> UserResponse:
    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=user.role.name,
        is_active=user.is_active,
        is_verified=user.is_verified,
    )

def admin_create_user(
    db: Session,
    payload: AdminCreateUserRequest,
) -> User:
    normalized_email = (
        str(payload.email)
        .strip()
        .lower()
    )

    existing_user = get_user_by_email(
        db,
        normalized_email,
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    role = get_role_by_name(
        db,
        payload.role.value,
    )

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Requested role is not configured.",
        )

    return create_user(
        db,
        full_name=payload.full_name,
        email=normalized_email,
        password_hash=hash_password(
            payload.password,
        ),
        role_id=role.id,
    )

def get_users(
    db: Session,
    *,
    page: int,
    page_size: int,
    search: str | None,
    role: UserRole | None,
    is_active: bool | None,
) -> UserListResponse:
    offset = (
        page - 1
    ) * page_size

    users, total = list_users(
        db,
        search=search,
        role=(
            role.value
            if role is not None
            else None
        ),
        is_active=is_active,
        offset=offset,
        limit=page_size,
    )

    total_pages = (
        math.ceil(
            total / page_size
        )
        if total
        else 0
    )

    return UserListResponse(
        items=[
            build_user_response(user)
            for user in users
        ],
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )

def get_user_or_404(
    db: Session,
    user_id: int,
) -> User:
    user = get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user

def update_user_status(
    db: Session,
    *,
    target_user: User,
    is_active: bool,
    acting_admin: User,
) -> User:
    if (
        target_user.id == acting_admin.id
        and not is_active
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot deactivate your own account.",
        )

    target_user.is_active = is_active

    return save_user(
        db,
        target_user,
    )

def update_user_role(
    db: Session,
    *,
    target_user: User,
    new_role: UserRole,
    acting_admin: User,
) -> User:
    if target_user.id == acting_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot change your own role.",
        )

    role = get_role_by_name(
        db,
        new_role.value,
    )

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Requested role is not configured.",
        )

    target_user.role_id = role.id

    return save_user(
        db,
        target_user,
    )