from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

from app.core.constants import UserRole


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    is_verified: bool


class UpdateProfileRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    full_name: str = Field(
        min_length=2,
        max_length=120,
    )

    email: EmailStr

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

class AdminCreateUserRequest(BaseModel):
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

    role: UserRole = UserRole.AGENT

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

class UpdateUserStatusRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    is_active: bool

class UpdateUserRoleRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    role: UserRole

class UserListResponse(BaseModel):
    items: list[UserResponse]
    page: int
    page_size: int
    total: int
    total_pages: int