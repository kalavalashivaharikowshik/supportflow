from fastapi.testclient import TestClient

from app.models.user import User


def test_login_returns_jwt(
    client: TestClient,
    requester: User,
):
    response = client.post(
        "/api/auth/login",
        json={
            "email": requester.email,
            "password": "Requester@123",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert body["user"]["role"] == "REQUESTER"


def test_wrong_password_returns_401(
    client: TestClient,
    requester: User,
):
    response = client.post(
        "/api/auth/login",
        json={
            "email": requester.email,
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401


def test_unknown_email_returns_401(
    client: TestClient,
):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "missing@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 401