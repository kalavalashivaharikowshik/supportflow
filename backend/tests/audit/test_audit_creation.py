from sqlalchemy import select

from app.core.constants import (
    AuditEventType,
)
from app.models.ticket_audit import (
    TicketAudit,
)
from tests.helpers import auth_headers


def test_assignment_creates_audit_event(
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

    audit = db.scalar(
        select(TicketAudit).where(
            TicketAudit.ticket_id
            == ticket.id,
            TicketAudit.event_type
            == (
                AuditEventType
                .TICKET_ASSIGNED
                .value
            ),
        )
    )

    assert audit is not None