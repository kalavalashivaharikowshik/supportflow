from datetime import timedelta

from sqlalchemy import select

from app.core.constants import (
    NotificationType,
    TicketStatus,
)
from app.models.notification import Notification
from app.services.escalation_service import (
    process_sla_escalations,
)
from app.utils.datetime import utc_now


def test_auto_reassignment_notifies_new_agent(
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

    notifications = db.scalars(
        select(Notification).where(
            Notification.ticket_id
            == overdue_ticket.id
        )
    ).all()

    matching = [
        notification
        for notification in notifications
        if (
            notification.user_id
            == agent_two.id
            and notification.type
            == NotificationType.TICKET_REASSIGNED.value
        )
    ]

    assert len(matching) == 1

def test_auto_reassignment_notifies_old_agent(
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

    notifications = db.scalars(
        select(Notification).where(
            Notification.ticket_id
            == overdue_ticket.id
        )
    ).all()

    matching = [
        notification
        for notification in notifications
        if (
            notification.user_id
            == agent.id
            and notification.type
            == NotificationType.TICKET_REASSIGNED.value
        )
    ]

    assert len(matching) == 1

def test_auto_reassignment_does_not_notify_unrelated_agent(
    db,
    requester,
    agent,
    agent_two,
    agent_three,
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

    ticket_factory(
        requester_id=requester.id,
        priority="LOW",
        status=TicketStatus.ASSIGNED.value,
        assigned_agent_id=agent_three.id,
    )

    db.flush()

    process_sla_escalations(
        db,
        now=now,
    )

    notifications = db.scalars(
        select(Notification).where(
            Notification.ticket_id
            == overdue_ticket.id
        )
    ).all()

    unrelated = [
        notification
        for notification in notifications
        if (
            notification.user_id
            == agent_three.id
            and notification.type
            == NotificationType.TICKET_REASSIGNED.value
        )
    ]

    assert len(unrelated) == 0