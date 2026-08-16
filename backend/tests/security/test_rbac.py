from fastapi.testclient import TestClient

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


def test_users_endpoint_without_auth_returns_401(
    client: TestClient,
):
    response = client.get(
        "/api/users"
    )

    assert response.status_code == 401