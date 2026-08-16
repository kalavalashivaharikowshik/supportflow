from fastapi.testclient import TestClient

from app.core.constants import TicketStatus
from app.models.user import User
from tests.helpers import auth_headers


def test_requester_can_add_public_response_to_own_ticket(
    client: TestClient,
    requester: User,
    requester_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
    )

    response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            requester_token
        ),
        json={
            "message": (
                "The issue is still affecting "
                "our users."
            ),
            "is_internal": False,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["ticket_id"] == ticket.id
    assert body["author_id"] == requester.id
    assert body["author_role"] == "REQUESTER"
    assert body["is_internal"] is False


def test_requester_cannot_add_internal_note(
    client: TestClient,
    requester: User,
    requester_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
    )

    response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            requester_token
        ),
        json={
            "message": (
                "Requester attempting an "
                "internal-only note."
            ),
            "is_internal": True,
        },
    )

    assert response.status_code == 403


def test_requester_cannot_respond_to_another_requesters_ticket(
    client: TestClient,
    requester: User,
    requester_two_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
    )

    response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            requester_two_token
        ),
        json={
            "message": (
                "Trying to respond to "
                "another requester's ticket."
            ),
            "is_internal": False,
        },
    )

    assert response.status_code == 403


def test_assigned_agent_can_add_public_response(
    client: TestClient,
    requester: User,
    agent: User,
    agent_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.ASSIGNED.value,
        assigned_agent_id=agent.id,
    )

    response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            agent_token
        ),
        json={
            "message": (
                "We have identified the issue "
                "and are investigating."
            ),
            "is_internal": False,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["author_role"] == "AGENT"
    assert body["is_internal"] is False


def test_assigned_agent_can_add_internal_note(
    client: TestClient,
    requester: User,
    agent: User,
    agent_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.IN_PROGRESS.value,
        assigned_agent_id=agent.id,
    )

    response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            agent_token
        ),
        json={
            "message": (
                "Internal investigation "
                "details for support staff."
            ),
            "is_internal": True,
        },
    )

    assert response.status_code == 201

    assert (
        response.json()["is_internal"]
        is True
    )


def test_unassigned_agent_cannot_respond(
    client: TestClient,
    requester: User,
    agent_two_token: str,
    agent: User,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.ASSIGNED.value,
        assigned_agent_id=agent.id,
    )

    response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            agent_two_token
        ),
        json={
            "message": (
                "Unassigned agent trying "
                "to respond."
            ),
            "is_internal": False,
        },
    )

    assert response.status_code == 403


def test_requester_conversation_hides_internal_notes(
    client: TestClient,
    requester: User,
    agent: User,
    requester_token: str,
    agent_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.IN_PROGRESS.value,
        assigned_agent_id=agent.id,
    )

    public_response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            agent_token
        ),
        json={
            "message": (
                "This is a public response."
            ),
            "is_internal": False,
        },
    )

    assert public_response.status_code == 201

    internal_response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            agent_token
        ),
        json={
            "message": (
                "This is an internal note."
            ),
            "is_internal": True,
        },
    )

    assert internal_response.status_code == 201

    conversation = client.get(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            requester_token
        ),
    )

    assert conversation.status_code == 200

    body = conversation.json()

    assert len(body["items"]) == 1

    for item in body["items"]:
        assert item["is_internal"] is False


def test_assigned_agent_conversation_can_see_internal_notes(
    client: TestClient,
    requester: User,
    agent: User,
    agent_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.IN_PROGRESS.value,
        assigned_agent_id=agent.id,
    )

    internal_response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            agent_token
        ),
        json={
            "message": (
                "Support-team-only internal note."
            ),
            "is_internal": True,
        },
    )

    assert internal_response.status_code == 201

    conversation = client.get(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            agent_token
        ),
    )

    assert conversation.status_code == 200

    body = conversation.json()

    assert any(
        item["is_internal"] is True
        for item in body["items"]
    )


def test_closed_ticket_cannot_receive_response(
    client: TestClient,
    requester: User,
    requester_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.CLOSED.value,
    )

    response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            requester_token
        ),
        json={
            "message": (
                "Attempting to respond "
                "after closure."
            ),
            "is_internal": False,
        },
    )

    assert response.status_code == 400


def test_blank_response_returns_422(
    client: TestClient,
    requester: User,
    requester_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
    )

    response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            requester_token
        ),
        json={
            "message": "   ",
            "is_internal": False,
        },
    )

    assert response.status_code == 422


def test_response_without_authentication_returns_401(
    client: TestClient,
    requester: User,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id,
    )

    response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        json={
            "message": (
                "Valid message but no "
                "authentication token."
            ),
            "is_internal": False,
        },
    )

    assert response.status_code == 401