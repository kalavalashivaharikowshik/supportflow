from fastapi.testclient import TestClient

from tests.helpers import auth_headers


def test_requester_dashboard_returns_expected_shape(
    client: TestClient,
    requester_token: str,
):
    response = client.get(
        "/api/dashboard/requester",
        headers=auth_headers(
            requester_token
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert "total_tickets" in body
    assert "open_tickets" in body
    assert "active_tickets" in body
    assert "resolved_tickets" in body
    assert "closed_tickets" in body
    assert "escalated_tickets" in body
    assert "sla_at_risk_tickets" in body

    assert "status_counts" in body
    assert "priority_counts" in body
    assert "recent_tickets" in body


def test_agent_dashboard_returns_expected_shape(
    client: TestClient,
    agent_token: str,
):
    response = client.get(
        "/api/dashboard/agent",
        headers=auth_headers(
            agent_token
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert "total_assigned_tickets" in body
    assert "active_tickets" in body
    assert "assigned_tickets" in body
    assert "in_progress_tickets" in body
    assert "escalated_tickets" in body
    assert "resolved_tickets" in body
    assert "sla_at_risk_tickets" in body

    assert "status_counts" in body
    assert "priority_counts" in body

    assert "average_first_response_minutes" in body
    assert "average_resolution_minutes" in body

    assert "recent_tickets" in body


def test_admin_dashboard_returns_expected_shape(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        "/api/dashboard/admin",
        headers=auth_headers(
            admin_token
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert "total_tickets" in body
    assert "open_tickets" in body
    assert "active_tickets" in body
    assert "resolved_tickets" in body
    assert "closed_tickets" in body

    assert "unassigned_tickets" in body
    assert "escalated_tickets" in body
    assert "sla_at_risk_tickets" in body

    assert "total_requesters" in body
    assert "total_agents" in body
    assert "active_agents" in body

    assert "status_counts" in body
    assert "priority_counts" in body

    assert "average_first_response_minutes" in body
    assert "average_resolution_minutes" in body

    assert "recent_tickets" in body
    assert "recent_escalations" in body
    assert "agent_workload" in body


def test_requester_cannot_access_admin_dashboard(
    client: TestClient,
    requester_token: str,
):
    response = client.get(
        "/api/dashboard/admin",
        headers=auth_headers(
            requester_token
        ),
    )

    assert response.status_code == 403


def test_requester_cannot_access_agent_dashboard(
    client: TestClient,
    requester_token: str,
):
    response = client.get(
        "/api/dashboard/agent",
        headers=auth_headers(
            requester_token
        ),
    )

    assert response.status_code == 403


def test_agent_cannot_access_admin_dashboard(
    client: TestClient,
    agent_token: str,
):
    response = client.get(
        "/api/dashboard/admin",
        headers=auth_headers(
            agent_token
        ),
    )

    assert response.status_code == 403


def test_agent_cannot_access_requester_dashboard(
    client: TestClient,
    agent_token: str,
):
    response = client.get(
        "/api/dashboard/requester",
        headers=auth_headers(
            agent_token
        ),
    )

    assert response.status_code == 403


def test_admin_cannot_access_requester_dashboard(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        "/api/dashboard/requester",
        headers=auth_headers(
            admin_token
        ),
    )

    assert response.status_code == 403


def test_admin_cannot_access_agent_dashboard(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        "/api/dashboard/agent",
        headers=auth_headers(
            admin_token
        ),
    )

    assert response.status_code == 403


def test_dashboard_without_authentication_returns_401(
    client: TestClient,
):
    requester_response = client.get(
        "/api/dashboard/requester"
    )

    agent_response = client.get(
        "/api/dashboard/agent"
    )

    admin_response = client.get(
        "/api/dashboard/admin"
    )

    assert requester_response.status_code == 401
    assert agent_response.status_code == 401
    assert admin_response.status_code == 401