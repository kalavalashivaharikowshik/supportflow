from datetime import (
    datetime,
    timedelta,
    timezone,
)

from app.core.constants import (
    TicketStatus,
)
from app.services.escalation_service import (
    should_escalate_ticket,
)


def test_ticket_before_sla_deadline_does_not_escalate(
    requester,
    ticket_factory,
):
    now = datetime(
        2026,
        8,
        15,
        10,
        0,
        tzinfo=timezone.utc,
    )

    ticket = ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.OPEN.value,
        created_at=(
            now - timedelta(hours=1)
        ),
        sla_deadline=(
            now + timedelta(seconds=1)
        ),
    )

    assert (
        should_escalate_ticket(
            ticket,
            now=now,
        )
        is False
    )


def test_ticket_exactly_at_sla_deadline_escalates(
    requester,
    ticket_factory,
):
    now = datetime(
        2026,
        8,
        15,
        10,
        0,
        tzinfo=timezone.utc,
    )

    ticket = ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.OPEN.value,
        created_at=(
            now - timedelta(hours=2)
        ),
        sla_deadline=now,
    )

    assert (
        should_escalate_ticket(
            ticket,
            now=now,
        )
        is True
    )


def test_ticket_after_sla_deadline_escalates(
    requester,
    ticket_factory,
):
    now = datetime(
        2026,
        8,
        15,
        10,
        0,
        tzinfo=timezone.utc,
    )

    ticket = ticket_factory(
        requester_id=requester.id,
        status=TicketStatus.OPEN.value,
        created_at=(
            now - timedelta(hours=3)
        ),
        sla_deadline=(
            now - timedelta(seconds=1)
        ),
    )

    assert (
        should_escalate_ticket(
            ticket,
            now=now,
        )
        is True
    )

def test_resolved_ticket_never_escalates(
    requester,
    ticket_factory,
):
    now = datetime.now(
        timezone.utc
    )

    ticket = ticket_factory(
        requester_id=requester.id,
        status=(
            TicketStatus.RESOLVED.value
        ),
        sla_deadline=(
            now - timedelta(hours=1)
        ),
    )

    assert (
        should_escalate_ticket(
            ticket,
            now=now,
        )
        is False
    )


def test_closed_ticket_never_escalates(
    requester,
    ticket_factory,
):
    now = datetime.now(
        timezone.utc
    )

    ticket = ticket_factory(
        requester_id=requester.id,
        status=(
            TicketStatus.CLOSED.value
        ),
        sla_deadline=(
            now - timedelta(hours=1)
        ),
    )

    assert (
        should_escalate_ticket(
            ticket,
            now=now,
        )
        is False
    )

def test_already_escalated_ticket_does_not_escalate_again(
    requester,
    ticket_factory,
):
    now = datetime.now(
        timezone.utc
    )

    ticket = ticket_factory(
        requester_id=requester.id,
        status=(
            TicketStatus.ESCALATED.value
        ),
        sla_deadline=(
            now - timedelta(hours=1)
        ),
        is_escalated=True,
    )

    assert (
        should_escalate_ticket(
            ticket,
            now=now,
        )
        is False
    )