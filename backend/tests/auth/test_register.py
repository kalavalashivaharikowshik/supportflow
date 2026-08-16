from fastapi.testclient import TestClient


def test_public_registration_creates_requester(
    client: TestClient,
):
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "New User",
            "email": "new@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["email"] == "new@test.com"
    assert body["role"] == "REQUESTER"

    assert "password" not in body
    assert "password_hash" not in body

def test_duplicate_registration_returns_409(
    client: TestClient,
):
    payload = {
        "full_name": "New User",
        "email": "duplicate@test.com",
        "password": "Password@123",
    }

    first = client.post(
        "/api/auth/register",
        json=payload,
    )

    assert first.status_code == 201

    second = client.post(
        "/api/auth/register",
        json=payload,
    )

    assert second.status_code == 409

def test_registration_rejects_role_injection(
    client: TestClient,
):
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Fake Admin",
            "email": "fakeadmin@test.com",
            "password": "Password@123",
            "role": "ADMIN",
        },
    )

    assert response.status_code == 422