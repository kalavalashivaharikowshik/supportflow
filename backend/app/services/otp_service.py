import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.password_otp import PasswordResetOTP
from app.models.user import User


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp(
    otp: str,
) -> str:
    value = (
        f"{otp}:{settings.jwt_secret_key}"
    ).encode()

    return hashlib.sha256(value).hexdigest()


def verify_otp_hash(
    plain_otp: str,
    stored_hash: str,
) -> bool:
    calculated_hash = hash_otp(
        plain_otp,
    )

    return hmac.compare_digest(
        calculated_hash,
        stored_hash,
    )


def invalidate_existing_otps(
    db: Session,
    user_id: int,
) -> None:
    statement = (
        update(PasswordResetOTP)
        .where(
            PasswordResetOTP.user_id == user_id,
            PasswordResetOTP.is_used.is_(False),
        )
        .values(
            is_used=True,
            used_at=utc_now(),
        )
    )

    db.execute(statement)


def create_password_reset_otp(
    db: Session,
    user: User,
) -> str:
    invalidate_existing_otps(
        db,
        user.id,
    )

    plain_otp = generate_otp()

    otp_record = PasswordResetOTP(
        user_id=user.id,
        otp_hash=hash_otp(plain_otp),
        expires_at=(
            utc_now()
            + timedelta(
                minutes=settings.otp_expire_minutes,
            )
        ),
    )

    db.add(otp_record)
    db.commit()

    return plain_otp


def get_latest_valid_otp(
    db: Session,
    user_id: int,
) -> PasswordResetOTP | None:
    statement = (
        select(PasswordResetOTP)
        .where(
            PasswordResetOTP.user_id == user_id,
            PasswordResetOTP.is_used.is_(False),
        )
        .order_by(
            PasswordResetOTP.created_at.desc(),
        )
    )

    return db.scalar(statement)


def verify_password_reset_otp(
    db: Session,
    user: User,
    plain_otp: str,
) -> PasswordResetOTP:
    otp_record = get_latest_valid_otp(
        db,
        user.id,
    )

    if otp_record is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active password reset request found.",
        )

    if otp_record.attempt_count >= settings.otp_max_attempts:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Maximum OTP verification attempts exceeded.",
        )

    now = utc_now()

    expires_at = otp_record.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(
            tzinfo=timezone.utc,
        )

    if now >= expires_at:
        otp_record.is_used = True
        otp_record.used_at = now

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired.",
        )

    if not verify_otp_hash(
        plain_otp,
        otp_record.otp_hash,
    ):
        otp_record.attempt_count += 1

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP.",
        )

    otp_record.is_verified = True
    otp_record.verified_at = now

    db.commit()
    db.refresh(otp_record)

    return otp_record