from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.api.dependencies.auth import get_current_user
from app.core.constants import UserRole
from app.models.user import User


def require_roles(
    *allowed_roles: UserRole,
) -> Callable:
    allowed_role_values = {
        role.value
        for role in allowed_roles
    }

    def dependency(
        current_user: Annotated[
            User,
            Depends(get_current_user),
        ],
    ) -> User:
        if current_user.role.name not in allowed_role_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return dependency


require_admin = require_roles(
    UserRole.ADMIN,
)

require_agent = require_roles(
    UserRole.AGENT,
)

require_requester = require_roles(
    UserRole.REQUESTER,
)

require_agent_or_admin = require_roles(
    UserRole.AGENT,
    UserRole.ADMIN,
)