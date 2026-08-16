from fastapi.testclient import TestClient

from app.models.user import User
from tests.helpers import auth_headers


def test_admin_assigns_ticket_to_agent(
    client: TestClient,
    requester: User,
    agent: User,
    admin_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id
    )

    response = client.patch(
        (
            f"/api/tickets/admin/"
            f"{ticket.id}/assign"
        ),
        headers=auth_headers(
            admin_token
        ),
        json={
            "agent_id": agent.id,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ASSIGNED"
    assert (
        body["assigned_agent_id"]
        == agent.id
    )


def test_requester_cannot_assign_ticket(
    client: TestClient,
    requester: User,
    agent: User,
    requester_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id
    )

    response = client.patch(
        (
            f"/api/tickets/admin/"
            f"{ticket.id}/assign"
        ),
        headers=auth_headers(
            requester_token
        ),
        json={
            "agent_id": agent.id,
        },
    )

    assert response.status_code == 403