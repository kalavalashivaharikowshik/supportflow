from sqlalchemy import select

from app.core.constants import UserRole
from app.core.security import hash_password
from app.db.database import SessionLocal
from app.db.seed import (
    seed_app_config,
    seed_roles,
    seed_sla_configs,
)
from app.models.role import Role
from app.models.user import User

E2E_USERS = [
    {
        "full_name": "E2E Requester",
        "email": "requester.e2e@example.com",
        "password": "Requester@123",
        "role": UserRole.REQUESTER,
    },
    {
        "full_name": "E2E Agent",
        "email": "agent.e2e@example.com",
        "password": "Agent@123",
        "role": UserRole.AGENT,
    },
    {
        "full_name": "E2E Agent Two",
        "email": "agent2.e2e@example.com",
        "password": "AgentTwo@123",
        "role": UserRole.AGENT,
    },
    {
        "full_name": "E2E Admin",
        "email": "admin.e2e@example.com",
        "password": "Admin@123",
        "role": UserRole.ADMIN,
    },
]


def get_role_by_name(
    db,
    role_name: str,
) -> Role:
    role = db.scalar(
        select(Role).where(
            Role.name == role_name
        )
    )

    if role is None:
        raise RuntimeError(
            f"Role not found: {role_name}"
        )

    return role


def seed_e2e_users() -> None:
    db = SessionLocal()

    try:
        for user_data in E2E_USERS:
            existing_user = db.scalar(
                select(User).where(
                    User.email
                    == user_data["email"]
                )
            )

            if existing_user is not None:
                continue

            role = get_role_by_name(
                db,
                user_data["role"].value,
            )

            db.add(
                User(
                    full_name=(
                        user_data[
                            "full_name"
                        ]
                    ),
                    email=(
                        user_data[
                            "email"
                        ]
                    ),
                    password_hash=(
                        hash_password(
                            user_data[
                                "password"
                            ]
                        )
                    ),
                    role_id=role.id,
                    is_active=True,
                    is_verified=True,
                )
            )

        db.commit()

    finally:
        db.close()


def seed_e2e_database() -> None:
    seed_roles()
    seed_sla_configs()
    seed_app_config()
    seed_e2e_users()

    print(
        "E2E database seeded successfully."
    )


if __name__ == "__main__":
    seed_e2e_database()