from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants import UserRole
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_role_by_name,
    get_user_by_email,
    save_user,
)
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
)
from app.services.otp_service import (
    create_password_reset_otp,
    verify_password_reset_otp,
)


def register_user(
    db: Session,
    payload: RegisterRequest,
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

    requester_role = get_role_by_name(
        db,
        UserRole.REQUESTER.value,
    )

    if requester_role is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default requester role is not configured.",
        )

    hashed_password = hash_password(
        payload.password,
    )

    return create_user(
        db,
        full_name=payload.full_name.strip(),
        email=normalized_email,
        password_hash=hashed_password,
        role_id=requester_role.id,
    )

def authenticate_user(
    db: Session,
    payload: LoginRequest,
) -> tuple[User, str]:
    normalized_email = (
        str(payload.email)
        .strip()
        .lower()
    )

    user = get_user_by_email(
        db,
        normalized_email,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive.",
        )

    user.last_login_at = datetime.now(
        timezone.utc,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(
        subject=str(user.id),
        extra_claims={
            "role": user.role.name,
        },
    )

    return user, access_token

def change_password(
    db: Session,
    user: User,
    current_password: str,
    new_password: str,
) -> None:
    if not verify_password(
        current_password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    if verify_password(
        new_password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "New password must be different "
                "from the current password."
            ),
        )

    user.password_hash = hash_password(
        new_password,
    )

    save_user(
        db,
        user,
    )

def request_password_reset(
    db: Session,
    email: str,
) -> tuple[User | None, str | None]:
    normalized_email = (
        email.strip().lower()
    )

    user = get_user_by_email(
        db,
        normalized_email,
    )

    if user is None:
        return None, None

    if not user.is_active:
        return None, None

    otp = create_password_reset_otp(
        db,
        user,
    )

    return user, otp

def reset_password_with_otp(
    db: Session,
    email: str,
    otp: str,
    new_password: str,
) -> None:
    normalized_email = (
        email.strip().lower()
    )

    user = get_user_by_email(
        db,
        normalized_email,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password reset request.",
        )

    otp_record = verify_password_reset_otp(
        db,
        user,
        otp,
    )

    if verify_password(
        new_password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "New password must be different "
                "from the current password."
            ),
        )

    user.password_hash = hash_password(
        new_password,
    )

    otp_record.is_used = True
    otp_record.used_at = datetime.now(
        timezone.utc,
    )

    db.add(user)
    db.add(otp_record)

    db.commit()