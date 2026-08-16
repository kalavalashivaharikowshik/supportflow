from datetime import (
    datetime,
    timedelta,
    timezone,
)

from app.core.constants import (
    TicketStatus,
)
from app.services.escalation_service import (
    process_sla_escalations,
)


def test_overdue_ticket_is_escalated(
    db,
    requester,
    ticket_factory,
):
    now = datetime.now(
        timezone.utc
    )

    ticket = ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.OPEN.value,
        sla_deadline=(
            now - timedelta(minutes=1)
        ),
    )

    escalated = process_sla_escalations(
        db,
        now=now,
    )

    assert len(escalated) == 1

    db.refresh(ticket)

    assert ticket.is_escalated is True
    assert (
        ticket.status
        == TicketStatus.ESCALATED.value
    )
    assert ticket.escalated_at is not None

def test_escalation_processing_is_idempotent(
    db,
    requester,
    ticket_factory,
):
    now = datetime.now(
        timezone.utc
    )

    ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.OPEN.value,
        sla_deadline=(
            now - timedelta(minutes=1)
        ),
    )

    first = process_sla_escalations(
        db,
        now=now,
    )

    second = process_sla_escalations(
        db,
        now=(
            now + timedelta(minutes=1)
        ),
    )

    assert len(first) == 1
    assert len(second) == 0