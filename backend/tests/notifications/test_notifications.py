from sqlalchemy import select

from app.core.constants import (
    NotificationType,
)
from app.models.notification import (
    Notification,
)
from tests.helpers import auth_headers


def test_assignment_creates_agent_notification(
    client,
    db,
    requester,
    agent,
    admin_token,
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

    notification = db.scalar(
        select(Notification).where(
            Notification.user_id
            == agent.id,
            Notification.ticket_id
            == ticket.id,
            Notification.type
            == (
                NotificationType
                .TICKET_ASSIGNED
                .value
            ),
        )
    )

    assert notification is not None
    assert notification.is_read is False