from fastapi.testclient import TestClient

from tests.helpers import auth_headers


def test_me_returns_authenticated_user(
    client: TestClient,
    requester_token: str,
):
    response = client.get(
        "/api/auth/me",
        headers=auth_headers(
            requester_token
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["role"] == "REQUESTER"


def test_me_without_token_returns_401(
    client: TestClient,
):
    response = client.get(
        "/api/auth/me"
    )

    assert response.status_code == 401


def test_me_invalid_token_returns_401(
    client: TestClient,
):
    response = client.get(
        "/api/auth/me",
        headers={
            "Authorization": (
                "Bearer invalid-token"
            )
        },
    )

    assert response.status_code == 401