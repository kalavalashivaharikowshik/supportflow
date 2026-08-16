from fastapi.testclient import TestClient

from app.models.user import User
from tests.helpers import auth_headers


def test_admin_can_list_users(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        "/api/users",
        headers=auth_headers(
            admin_token
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert "items" in body
    assert "page" in body
    assert "page_size" in body
    assert "total" in body
    assert "total_pages" in body


def test_requester_cannot_list_users(
    client: TestClient,
    requester_token: str,
):
    response = client.get(
        "/api/users",
        headers=auth_headers(
            requester_token
        ),
    )

    assert response.status_code == 403


def test_agent_cannot_list_users(
    client: TestClient,
    agent_token: str,
):
    response = client.get(
        "/api/users",
        headers=auth_headers(
            agent_token
        ),
    )

    assert response.status_code == 403


def test_admin_can_get_user_by_id(
    client: TestClient,
    admin_token: str,
    requester: User,
):
    response = client.get(
        f"/api/users/{requester.id}",
        headers=auth_headers(
            admin_token
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == requester.id
    assert body["email"] == requester.email
    assert body["role"] == "REQUESTER"


def test_admin_get_missing_user_returns_404(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        "/api/users/999999",
        headers=auth_headers(
            admin_token
        ),
    )

    assert response.status_code == 404


def test_admin_can_create_agent(
    client: TestClient,
    admin_token: str,
):
    response = client.post(
        "/api/users",
        headers=auth_headers(
            admin_token
        ),
        json={
            "full_name": "Created Agent",
            "email": "created.agent@test.com",
            "password": "AgentTest@123",
            "role": "AGENT",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["email"] == "created.agent@test.com"
    assert body["role"] == "AGENT"
    assert body["is_active"] is True

    assert "password" not in body
    assert "password_hash" not in body


def test_requester_cannot_create_user(
    client: TestClient,
    requester_token: str,
):
    response = client.post(
        "/api/users",
        headers=auth_headers(
            requester_token
        ),
        json={
            "full_name": "Forbidden Agent",
            "email": "forbidden.agent@test.com",
            "password": "AgentTest@123",
            "role": "AGENT",
        },
    )

    assert response.status_code == 403


def test_admin_can_deactivate_user(
    client: TestClient,
    admin_token: str,
    agent: User,
):
    response = client.patch(
        f"/api/users/{agent.id}/status",
        headers=auth_headers(
            admin_token
        ),
        json={
            "is_active": False,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == agent.id
    assert body["is_active"] is False


def test_admin_can_reactivate_user(
    client: TestClient,
    admin_token: str,
    agent: User,
):
    deactivate = client.patch(
        f"/api/users/{agent.id}/status",
        headers=auth_headers(
            admin_token
        ),
        json={
            "is_active": False,
        },
    )

    assert deactivate.status_code == 200

    reactivate = client.patch(
        f"/api/users/{agent.id}/status",
        headers=auth_headers(
            admin_token
        ),
        json={
            "is_active": True,
        },
    )

    assert reactivate.status_code == 200
    assert (
        reactivate.json()["is_active"]
        is True
    )


def test_users_without_authentication_returns_401(
    client: TestClient,
):
    response = client.get(
        "/api/users"
    )

    assert response.status_code == 401