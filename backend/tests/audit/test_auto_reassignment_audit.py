from datetime import timedelta

from sqlalchemy import select

from app.core.constants import (
    AuditEventType,
    TicketStatus,
)
from app.models.ticket_audit import TicketAudit
from app.services.escalation_service import (
    process_sla_escalations,
)
from app.utils.datetime import utc_now


def test_sla_auto_reassignment_creates_both_audit_events(
    db,
    requester,
    agent,
    agent_two,
    ticket_factory,
):
    now = utc_now()

    overdue_ticket = ticket_factory(
        requester_id=requester.id,
        priority="HIGH",
        status=TicketStatus.ASSIGNED.value,
        assigned_agent_id=agent.id,
        sla_deadline=(
            now - timedelta(minutes=1)
        ),
    )

    db.flush()

    process_sla_escalations(
        db,
        now=now,
    )

    events = db.scalars(
        select(TicketAudit).where(
            TicketAudit.ticket_id
            == overdue_ticket.id
        )
    ).all()

    sla_events = [
        event
        for event in events
        if (
            event.event_type
            == AuditEventType.SLA_ESCALATED.value
        )
    ]

    reassignment_events = [
        event
        for event in events
        if (
            event.event_type
            == AuditEventType.TICKET_REASSIGNED.value
        )
    ]

    assert len(sla_events) == 1
    assert len(reassignment_events) == 1

    reassignment_event = (
        reassignment_events[0]
    )

    assert (
        str(agent.id)
        in reassignment_event.old_value
    )

    assert (
        str(agent_two.id)
        in reassignment_event.new_value
    )