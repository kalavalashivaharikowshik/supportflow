from fastapi.testclient import TestClient

from app.models.user import User
from tests.helpers import auth_headers


def test_full_ticket_lifecycle(
    client: TestClient,
    requester: User,
    agent: User,
    requester_token: str,
    agent_token: str,
    admin_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id
    )

    assignment = client.patch(
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

    assert assignment.status_code == 200

    started = client.patch(
        (
            f"/api/tickets/assigned/"
            f"{ticket.id}/start"
        ),
        headers=auth_headers(
            agent_token
        ),
    )

    assert started.status_code == 200
    assert (
        started.json()["status"]
        == "IN_PROGRESS"
    )

    resolved = client.patch(
        (
            f"/api/tickets/assigned/"
            f"{ticket.id}/resolve"
        ),
        headers=auth_headers(
            agent_token
        ),
        json={
            "resolution_summary": (
                "The underlying issue was "
                "fixed and validated."
            ),
        },
    )

    assert resolved.status_code == 200
    assert (
        resolved.json()["status"]
        == "RESOLVED"
    )

    closed = client.patch(
        f"/api/tickets/{ticket.id}/close",
        headers=auth_headers(
            requester_token
        ),
    )

    assert closed.status_code == 200
    assert (
        closed.json()["status"]
        == "CLOSED"
    )

def test_assigned_ticket_cannot_be_resolved_without_start(
    client: TestClient,
    requester: User,
    agent: User,
    agent_token: str,
    admin_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id
    )

    assignment = client.patch(
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

    assert assignment.status_code == 200

    resolved = client.patch(
        (
            f"/api/tickets/assigned/"
            f"{ticket.id}/resolve"
        ),
        headers=auth_headers(
            agent_token
        ),
        json={
            "resolution_summary": (
                "Attempting an invalid "
                "direct resolution."
            ),
        },
    )

    assert resolved.status_code == 400