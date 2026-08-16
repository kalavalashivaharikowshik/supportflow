import os
from collections.abc import Generator

os.environ["TESTING"] = "true"

os.environ["DATABASE_URL"] = (
    "sqlite:///./test_supportflow.db"
)

os.environ["ALLOWED_HOSTS"] = (
    "127.0.0.1,localhost,testserver"
)

from datetime import (
    datetime,
    timedelta,
    timezone,
)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.core.constants import (
    TicketStatus,
)
from app.core.security import hash_password
from app.db.base import Base
from app.db.database import get_db
from app.main import app
from app.models import (
    Role,
    SLAConfig,
    Ticket,
    User,
)
from tests.helpers import login_user

TEST_DATABASE_URL = (
    "sqlite:///./test_supportflow.db"
)


engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(
    scope="session",
    autouse=True,
)
def create_test_database() -> Generator[
    None,
    None,
    None,
]:
    Base.metadata.drop_all(
        bind=engine
    )

    Base.metadata.create_all(
        bind=engine
    )

    yield

    Base.metadata.drop_all(
        bind=engine
    )


@pytest.fixture
def db() -> Generator[
    Session,
    None,
    None,
]:
    connection = engine.connect()

    transaction = connection.begin()

    session = TestingSessionLocal(
        bind=connection
    )

    yield session

    session.close()

    transaction.rollback()

    connection.close()


@pytest.fixture
def client(
    db: Session,
) -> Generator[
    TestClient,
    None,
    None,
]:
    def override_get_db():
        yield db

    app.dependency_overrides[
        get_db
    ] = override_get_db

    with TestClient(
        app,
        raise_server_exceptions=False,
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture(
    autouse=True,
)
def seed_reference_data(
    db: Session,
):
    roles = [
        "REQUESTER",
        "AGENT",
        "ADMIN",
    ]

    for role_name in roles:
        db.add(
            Role(
                name=role_name,
            )
        )

    sla_values = {
        "LOW": 4320,
        "MEDIUM": 1440,
        "HIGH": 480,
        "CRITICAL": 120,
    }

    for priority, minutes in (
        sla_values.items()
    ):
        db.add(
            SLAConfig(
                priority=priority,
                resolution_minutes=minutes,
                is_active=True,
            )
        )

    db.flush()

@pytest.fixture
def user_factory(
    db: Session,
):
    def create_user(
        *,
        email: str,
        password: str,
        full_name: str,
        role_name: str,
        is_active: bool = True,
    ) -> User:
        role = db.scalar(
            select(Role).where(
                Role.name == role_name
            )
        )

        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(
                password
            ),
            role_id=role.id,
            is_active=is_active,
            is_verified=True,
        )

        db.add(user)
        db.flush()

        return user

    return create_user

@pytest.fixture
def requester(
    user_factory,
) -> User:
    return user_factory(
        email="requester@test.com",
        password="Requester@123",
        full_name="Test Requester",
        role_name="REQUESTER",
    )


@pytest.fixture
def requester_two(
    user_factory,
) -> User:
    return user_factory(
        email="requester2@test.com",
        password="RequesterTwo@123",
        full_name="Second Requester",
        role_name="REQUESTER",
    )


@pytest.fixture
def agent(
    user_factory,
) -> User:
    return user_factory(
        email="agent@test.com",
        password="Agent@123",
        full_name="Test Agent",
        role_name="AGENT",
    )


@pytest.fixture
def agent_two(
    user_factory,
) -> User:
    return user_factory(
        email="agent2@test.com",
        password="AgentTwo@123",
        full_name="Second Agent",
        role_name="AGENT",
    )

@pytest.fixture
def agent_three(
    user_factory,
) -> User:
    return user_factory(
        email="agent3@test.com",
        password="AgentThree@123",
        full_name="Third Agent",
        role_name="AGENT",
    )

@pytest.fixture
def admin(
    user_factory,
) -> User:
    return user_factory(
        email="admin@test.com",
        password="Admin@123",
        full_name="Test Admin",
        role_name="ADMIN",
    )

@pytest.fixture
def requester_token(
    client: TestClient,
    requester: User,
) -> str:
    return login_user(
        client,
        email=requester.email,
        password="Requester@123",
    )


@pytest.fixture
def requester_two_token(
    client: TestClient,
    requester_two: User,
) -> str:
    return login_user(
        client,
        email=requester_two.email,
        password="RequesterTwo@123",
    )


@pytest.fixture
def agent_token(
    client: TestClient,
    agent: User,
) -> str:
    return login_user(
        client,
        email=agent.email,
        password="Agent@123",
    )


@pytest.fixture
def agent_two_token(
    client: TestClient,
    agent_two: User,
) -> str:
    return login_user(
        client,
        email=agent_two.email,
        password="AgentTwo@123",
    )


@pytest.fixture
def admin_token(
    client: TestClient,
    admin: User,
) -> str:
    return login_user(
        client,
        email=admin.email,
        password="Admin@123",
    )

@pytest.fixture
def ticket_factory(
    db: Session,
):
    counter = {
        "value": 0,
    }

    def create_ticket(
        *,
        requester_id: int,
        priority: str = "HIGH",
        status: str = (
            TicketStatus.OPEN.value
        ),
        assigned_agent_id: int | None = None,
        created_at: datetime | None = None,
        sla_deadline: datetime | None = None,
        is_escalated: bool = False,
    ) -> Ticket:
        counter["value"] += 1

        now = (
            created_at
            or datetime.now(
                timezone.utc
            )
        )

        deadline = (
            sla_deadline
            or now
            + timedelta(hours=8)
        )

        ticket = Ticket(
            ticket_number=(
                "SUP-2026-"
                f"{counter['value']:06d}"
            ),
            title=(
                f"Test Ticket "
                f"{counter['value']}"
            ),
            description=(
                "This is a valid automated "
                "test ticket description."
            ),
            category="TECHNICAL",
            priority=priority,
            status=status,
            requester_id=requester_id,
            assigned_agent_id=(
                assigned_agent_id
            ),
            sla_deadline=deadline,
            created_at=now,
            updated_at=now,
            is_escalated=(
                is_escalated
            ),
        )

        db.add(ticket)
        db.flush()

        return ticket

    return create_ticket