from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

from app.schemas.user import UserResponse


class RegisterRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    full_name: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    @field_validator("full_name")
    @classmethod
    def validate_full_name(
        cls,
        value: str,
    ) -> str:
        normalized = value.strip()

        if len(normalized) < 2:
            raise ValueError(
                "Full name must contain at least 2 characters."
            )

        return normalized

class RegisterResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    is_verified: bool


class MessageResponse(BaseModel):
    message: str

class LoginRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    email: EmailStr
    password: str = Field(
        min_length=1,
        max_length=128,
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse

class ChangePasswordRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    current_password: str = Field(
        min_length=1,
        max_length=128,
    )

    new_password: str = Field(
        min_length=8,
        max_length=128,
    )

    confirm_password: str = Field(
        min_length=8,
        max_length=128,
    )

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(
        cls,
        value: str,
        info,
    ) -> str:
        new_password = info.data.get(
            "new_password"
        )

        if (
            new_password is not None
            and value != new_password
        ):
            raise ValueError(
                "New password and confirmation do not match."
            )

        return value

class ForgotPasswordRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    email: EmailStr


class VerifyOTPRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    email: EmailStr

    otp: str = Field(
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$",
    )


class ResetPasswordRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    email: EmailStr

    otp: str = Field(
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$",
    )

    new_password: str = Field(
        min_length=8,
        max_length=128,
    )

    confirm_password: str = Field(
        min_length=8,
        max_length=128,
    )

    @field_validator("confirm_password")
    @classmethod
    def reset_passwords_match(
        cls,
        value: str,
        info,
    ) -> str:
        new_password = info.data.get(
            "new_password"
        )

        if (
            new_password is not None
            and value != new_password
        ):
            raise ValueError(
                "New password and confirmation do not match."
            )

        return value