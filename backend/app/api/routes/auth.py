from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.config import settings
from app.core.exceptions import (
    RateLimitException,
)
from app.core.rate_limit import (
    login_rate_limiter,
    otp_rate_limiter,
)
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repository import (
    get_user_by_email,
)
from app.schemas.auth import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    RegisterResponse,
    ResetPasswordRequest,
    TokenResponse,
    VerifyOTPRequest,
)
from app.schemas.user import (
    UpdateProfileRequest,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    change_password,
    register_user,
    request_password_reset,
    reset_password_with_otp,
)
from app.services.email_service import (
    send_password_reset_otp_email,
)
from app.services.otp_service import (
    verify_password_reset_otp,
)
from app.services.user_service import (
    update_profile,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
):
    user = register_user(
        db,
        payload,
    )

    return RegisterResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=user.role.name,
        is_active=user.is_active,
        is_verified=user.is_verified,
    )

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: Request,
    payload: LoginRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    normalized_email = (
        str(payload.email)
        .strip()
        .lower()
    )

    rate_key = (
        f"{client_ip}:"
        f"{normalized_email}"
    )

    if not login_rate_limiter.is_allowed(
        rate_key
    ):
        raise RateLimitException()

    try:
        user, access_token = (
            authenticate_user(
                db,
                payload,
            )
        )

    except HTTPException:
        login_rate_limiter.record_attempt(
            rate_key
        )
        raise

    login_rate_limiter.reset(
        rate_key
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=(
            settings.access_token_expire_minutes
            * 60
        ),
        user=UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            role=user.role.name,
            is_active=user.is_active,
            is_verified=user.is_verified,
        ),
    )

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return UserResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        role=current_user.role.name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
    )

@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return MessageResponse(
        message="Logged out successfully.",
    )

@router.patch(
    "/me",
    response_model=UserResponse,
)
def update_me(
    payload: UpdateProfileRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    user = update_profile(
        db,
        current_user,
        payload,
    )

    return UserResponse(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=user.role.name,
        is_active=user.is_active,
        is_verified=user.is_verified,
    )

@router.post(
    "/change-password",
    response_model=MessageResponse,
)
def update_password(
    payload: ChangePasswordRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    change_password(
        db,
        current_user,
        payload.current_password,
        payload.new_password,
    )

    return MessageResponse(
        message="Password changed successfully.",
    )

@router.post(
    "/forgot-password",
    response_model=MessageResponse,
)
def forgot_password(
    request: Request,
    payload: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    normalized_email = (
        str(payload.email)
        .strip()
        .lower()
    )

    rate_key = (
        f"forgot:{client_ip}:"
        f"{normalized_email}"
    )

    if not otp_rate_limiter.is_allowed(
        rate_key
    ):
        raise RateLimitException(
            message=(
                "Too many password reset requests. "
                "Please try again later."
            )
        )

    otp_rate_limiter.record_attempt(
        rate_key
    )

    user, otp = request_password_reset(
        db,
        normalized_email,
    )

    if (
        user is not None
        and otp is not None
    ):
        background_tasks.add_task(
            send_password_reset_otp_email,
            user.email,
            otp,
        )

    return MessageResponse(
        message=(
            "If an account exists for that email, "
            "a password reset OTP has been sent."
        ),
    )

@router.post(
    "/verify-reset-otp",
    response_model=MessageResponse,
)
def verify_reset_otp(
    request: Request,
    payload: VerifyOTPRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    client_ip = (
        request.client.host
        if request.client
        else "unknown"
    )

    normalized_email = (
        str(payload.email)
        .strip()
        .lower()
    )

    rate_key = (
        f"verify:{client_ip}:"
        f"{normalized_email}"
    )

    if not otp_rate_limiter.is_allowed(
        rate_key
    ):
        raise RateLimitException(
            message=(
                "Too many OTP verification attempts. "
                "Please try again later."
            )
        )

    user = get_user_by_email(
        db,
        normalized_email,
    )

    if user is None:
        otp_rate_limiter.record_attempt(
            rate_key
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password reset request.",
        )

    try:
        verify_password_reset_otp(
            db,
            user,
            payload.otp,
        )

    except HTTPException:
        otp_rate_limiter.record_attempt(
            rate_key
        )
        raise

    otp_rate_limiter.reset(
        rate_key
    )

    return MessageResponse(
        message="OTP verified successfully.",
    )

@router.post(
    "/reset-password",
    response_model=MessageResponse,
)
def reset_password(
    payload: ResetPasswordRequest,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    reset_password_with_otp(
        db,
        str(payload.email),
        payload.otp,
        payload.new_password,
    )

    return MessageResponse(
        message="Password reset successfully.",
    )