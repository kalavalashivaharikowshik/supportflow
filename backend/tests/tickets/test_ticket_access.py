from fastapi.testclient import TestClient

from app.models.user import User
from tests.helpers import auth_headers


def test_requester_cannot_access_another_requesters_ticket(
    client: TestClient,
    requester: User,
    requester_two_token: str,
    ticket_factory,
):
    ticket = ticket_factory(
        requester_id=requester.id
    )

    response = client.get(
        f"/api/tickets/{ticket.id}",
        headers=auth_headers(
            requester_two_token
        ),
    )

    assert response.status_code == 403