from fastapi.testclient import TestClient

from tests.helpers import auth_headers


def test_admin_can_list_sla_configs(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        "/api/sla/configs",
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200

    body = response.json()

    priorities = {
        item["priority"]
        for item in body
    }

    assert priorities == {
        "LOW",
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    }


def test_requester_cannot_list_sla_configs(
    client: TestClient,
    requester_token: str,
):
    response = client.get(
        "/api/sla/configs",
        headers=auth_headers(requester_token),
    )

    assert response.status_code == 403


def test_agent_cannot_list_sla_configs(
    client: TestClient,
    agent_token: str,
):
    response = client.get(
        "/api/sla/configs",
        headers=auth_headers(agent_token),
    )

    assert response.status_code == 403


def test_admin_can_update_high_sla(
    client: TestClient,
    admin_token: str,
):
    response = client.patch(
        "/api/sla/configs/HIGH",
        headers=auth_headers(admin_token),
        json={
            "resolution_minutes": 600,
            "is_active": True,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["priority"] == "HIGH"
    assert body["resolution_minutes"] == 600
    assert body["is_active"] is True


def test_requester_cannot_update_sla_config(
    client: TestClient,
    requester_token: str,
):
    response = client.patch(
        "/api/sla/configs/HIGH",
        headers=auth_headers(requester_token),
        json={
            "resolution_minutes": 600,
            "is_active": True,
        },
    )

    assert response.status_code == 403


def test_invalid_zero_sla_duration_returns_422(
    client: TestClient,
    admin_token: str,
):
    response = client.patch(
        "/api/sla/configs/HIGH",
        headers=auth_headers(admin_token),
        json={
            "resolution_minutes": 0,
            "is_active": True,
        },
    )

    assert response.status_code == 422


def test_invalid_large_sla_duration_returns_422(
    client: TestClient,
    admin_token: str,
):
    response = client.patch(
        "/api/sla/configs/HIGH",
        headers=auth_headers(admin_token),
        json={
            "resolution_minutes": 50000,
            "is_active": True,
        },
    )

    assert response.status_code == 422


def test_invalid_sla_priority_returns_422(
    client: TestClient,
    admin_token: str,
):
    response = client.patch(
        "/api/sla/configs/URGENT",
        headers=auth_headers(admin_token),
        json={
            "resolution_minutes": 120,
            "is_active": True,
        },
    )

    assert response.status_code == 422


def test_disabled_sla_prevents_ticket_creation(
    client: TestClient,
    admin_token: str,
    requester_token: str,
):
    disable_response = client.patch(
        "/api/sla/configs/LOW",
        headers=auth_headers(admin_token),
        json={
            "resolution_minutes": 4320,
            "is_active": False,
        },
    )

    assert disable_response.status_code == 200

    ticket_response = client.post(
        "/api/tickets",
        headers=auth_headers(requester_token),
        json={
            "title": "Disabled SLA test",
            "description": (
                "Testing that ticket creation fails "
                "when the selected SLA is inactive."
            ),
            "category": "GENERAL",
            "priority": "LOW",
        },
    )

    assert ticket_response.status_code == 400


def test_ticket_uses_database_backed_sla_duration(
    client: TestClient,
    admin_token: str,
    requester_token: str,
):
    update_response = client.patch(
        "/api/sla/configs/HIGH",
        headers=auth_headers(admin_token),
        json={
            "resolution_minutes": 600,
            "is_active": True,
        },
    )

    assert update_response.status_code == 200

    ticket_response = client.post(
        "/api/tickets",
        headers=auth_headers(requester_token),
        json={
            "title": "Database SLA test",
            "description": (
                "Testing that ticket SLA deadline "
                "uses the database configuration."
            ),
            "category": "GENERAL",
            "priority": "HIGH",
        },
    )

    assert ticket_response.status_code == 201

    body = ticket_response.json()

    from datetime import datetime

    created = datetime.fromisoformat(
        body["created_at"].replace(
            "Z",
            "+00:00",
        )
    )

    deadline = datetime.fromisoformat(
        body["sla_deadline"].replace(
            "Z",
            "+00:00",
        )
    )

    difference_minutes = (
        deadline - created
    ).total_seconds() / 60

    assert abs(
        difference_minutes - 600
    ) < 0.1


def test_sla_configs_without_authentication_return_401(
    client: TestClient,
):
    response = client.get(
        "/api/sla/configs"
    )

    assert response.status_code == 401