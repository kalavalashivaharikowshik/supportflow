from fastapi.testclient import TestClient

from tests.helpers import auth_headers


def test_requester_can_create_ticket(
    client: TestClient,
    requester_token: str,
):
    response = client.post(
        "/api/tickets",
        headers=auth_headers(
            requester_token
        ),
        json={
            "title": "Production API failure",
            "description": (
                "The production API is currently "
                "returning errors to all users."
            ),
            "category": "TECHNICAL",
            "priority": "CRITICAL",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["status"] == "OPEN"
    assert body["assigned_agent_id"] is None
    assert body["is_escalated"] is False


def test_agent_cannot_create_ticket(
    client: TestClient,
    agent_token: str,
):
    response = client.post(
        "/api/tickets",
        headers=auth_headers(
            agent_token
        ),
        json={
            "title": "Test Ticket",
            "description": (
                "This description is long "
                "enough for validation."
            ),
            "category": "GENERAL",
            "priority": "LOW",
        },
    )

    assert response.status_code == 403