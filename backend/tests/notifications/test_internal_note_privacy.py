from sqlalchemy import func, select

from app.core.constants import TicketStatus
from app.models.notification import Notification
from app.models.user import User
from tests.helpers import auth_headers


def test_internal_note_does_not_notify_requester(
    client,
    db,
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

    before_count = db.scalar(
        select(
            func.count(Notification.id)
        ).where(
            Notification.user_id
            == requester.id,
            Notification.ticket_id
            == ticket.id,
        )
    ) or 0

    response = client.post(
        f"/api/tickets/{ticket.id}/responses",
        headers=auth_headers(
            agent_token
        ),
        json={
            "message": (
                "Internal investigation indicates "
                "a database connection issue."
            ),
            "is_internal": True,
        },
    )

    assert response.status_code == 201
    assert response.json()["is_internal"] is True

    after_count = db.scalar(
        select(
            func.count(Notification.id)
        ).where(
            Notification.user_id
            == requester.id,
            Notification.ticket_id
            == ticket.id,
        )
    ) or 0

    assert after_count == before_count