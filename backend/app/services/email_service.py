import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_password_reset_otp_email(
    recipient_email: str,
    otp: str,
) -> None:
    if (
        not settings.smtp_host
        or not settings.smtp_username
        or not settings.smtp_password
        or not settings.smtp_from_email
    ):
        raise RuntimeError(
            "SMTP configuration is incomplete."
        )

    message = EmailMessage()

    message["Subject"] = (
        "SupportFlow Password Reset OTP"
    )

    message["From"] = (
        f"{settings.smtp_from_name} "
        f"<{settings.smtp_from_email}>"
    )

    message["To"] = recipient_email

    message.set_content(
        (
            "You requested a password reset for your "
            "SupportFlow account.\n\n"
            f"Your OTP is: {otp}\n\n"
            f"This OTP expires in "
            f"{settings.otp_expire_minutes} minutes.\n\n"
            "If you did not request this password reset, "
            "you can ignore this email."
        )
    )

    with smtplib.SMTP(
        settings.smtp_host,
        settings.smtp_port,
        timeout=15,
    ) as smtp:
        smtp.starttls()

        smtp.login(
            settings.smtp_username,
            settings.smtp_password,
        )

        smtp.send_message(
            message,
        )