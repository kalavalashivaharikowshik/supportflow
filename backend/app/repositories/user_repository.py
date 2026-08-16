from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(
        User.email == email,
    )

    return db.scalar(statement)


def get_role_by_name(
    db: Session,
    role_name: str,
) -> Role | None:
    statement = select(Role).where(
        Role.name == role_name,
    )

    return db.scalar(statement)


def create_user(
    db: Session,
    *,
    full_name: str,
    email: str,
    password_hash: str,
    role_id: int,
) -> User:
    user = User(
        full_name=full_name,
        email=email,
        password_hash=password_hash,
        role_id=role_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    statement = select(User).where(
        User.id == user_id,
    )

    return db.scalar(statement)

def save_user(
    db: Session,
    user: User,
) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def list_users(
    db: Session,
    *,
    search: str | None,
    role: str | None,
    is_active: bool | None,
    offset: int,
    limit: int,
) -> tuple[list[User], int]:
    filters = []

    if search:
        pattern = f"%{search.strip()}%"

        filters.append(
            or_(
                User.full_name.ilike(pattern),
                User.email.ilike(pattern),
            )
        )

    if role:
        filters.append(
            User.role.has(
                Role.name == role,
            )
        )

    if is_active is not None:
        filters.append(
            User.is_active == is_active,
        )

    statement = (
        select(User)
        .where(*filters)
        .order_by(User.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    count_statement = (
        select(func.count(User.id))
        .where(*filters)
    )

    users = list(
        db.scalars(statement).all()
    )

    total = db.scalar(
        count_statement
    ) or 0

    return users, total

def list_active_agents(
    db: Session,
) -> list[User]:
    statement = (
        select(User)
        .where(
            User.is_active.is_(True),
            User.role.has(
                Role.name == "AGENT",
            ),
        )
        .order_by(
            User.full_name.asc()
        )
    )

    return list(
        db.scalars(statement).all()
    )

def list_active_admins(
    db: Session,
) -> list[User]:
    statement = (
        select(User)
        .where(
            User.is_active.is_(True),
            User.role.has(
                Role.name == "ADMIN",
            ),
        )
        .order_by(
            User.id.asc()
        )
    )

    return list(
        db.scalars(statement).all()
    )