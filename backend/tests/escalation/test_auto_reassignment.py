from datetime import timedelta

from sqlalchemy import select

from app.core.constants import (
    AuditEventType,
    NotificationType,
    TicketStatus,
)
from app.models.notification import Notification
from app.models.ticket_audit import TicketAudit
from app.services.escalation_service import (
    process_sla_escalations,
)
from app.utils.datetime import utc_now


def test_overdue_ticket_auto_reassigns_to_least_loaded_agent(
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

    ticket_factory(
        requester_id=requester.id,
        priority="LOW",
        status=TicketStatus.IN_PROGRESS.value,
        assigned_agent_id=agent_three.id,
    )

    db.flush()

    process_sla_escalations(
        db,
        now=now,
    )

    db.refresh(
        overdue_ticket
    )

    assert (
        overdue_ticket.status
        == TicketStatus.ESCALATED.value
    )

    assert (
        overdue_ticket.assigned_agent_id
        == agent_two.id
    )


def test_auto_reassignment_excludes_current_agent(
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

    db.refresh(
        overdue_ticket
    )

    assert (
        overdue_ticket.status
        == TicketStatus.ESCALATED.value
    )

    assert (
        overdue_ticket.assigned_agent_id
        == agent_two.id
    )


def test_auto_reassignment_ignores_inactive_agent(
    db,
    requester,
    agent,
    agent_two,
    agent_three,
    ticket_factory,
):
    now = utc_now()

    agent_two.is_active = False

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

    db.refresh(
        overdue_ticket
    )

    assert (
        overdue_ticket.assigned_agent_id
        == agent_three.id
    )

def test_auto_reassignment_respects_agent_capacity(
    db,
    requester,
    agent,
    agent_two,
    agent_three,
    ticket_factory,
):
    from app.services.app_config_service import (
        get_or_create_app_config,
    )

    now = utc_now()

    config = get_or_create_app_config(
        db
    )

    config.max_active_tickets_per_agent = 1

    ticket_factory(
        requester_id=requester.id,
        priority="LOW",
        status=TicketStatus.ASSIGNED.value,
        assigned_agent_id=agent_two.id,
    )

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

    db.refresh(
        overdue_ticket
    )

    assert (
        overdue_ticket.assigned_agent_id
        == agent_three.id
    )

def test_escalation_keeps_current_agent_when_no_replacement_exists(
    db,
    requester,
    agent,
    agent_two,
    agent_three,
    ticket_factory,
):
    from app.services.app_config_service import (
        get_or_create_app_config,
    )

    now = utc_now()

    config = get_or_create_app_config(
        db
    )

    config.max_active_tickets_per_agent = 1

    ticket_factory(
        requester_id=requester.id,
        priority="LOW",
        status=TicketStatus.ASSIGNED.value,
        assigned_agent_id=agent_two.id,
    )

    ticket_factory(
        requester_id=requester.id,
        priority="LOW",
        status=TicketStatus.ASSIGNED.value,
        assigned_agent_id=agent_three.id,
    )

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

    db.refresh(
        overdue_ticket
    )

    assert (
        overdue_ticket.status
        == TicketStatus.ESCALATED.value
    )

    assert (
        overdue_ticket.assigned_agent_id
        == agent.id
    )

def test_auto_reassignment_can_be_disabled(
    db,
    requester,
    agent,
    agent_two,
    ticket_factory,
):
    from app.services.app_config_service import (
        get_or_create_app_config,
    )

    now = utc_now()

    config = get_or_create_app_config(
        db
    )

    config.auto_reassign_on_escalation = False

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

    db.refresh(
        overdue_ticket
    )

    assert (
        overdue_ticket.status
        == TicketStatus.ESCALATED.value
    )

    assert (
        overdue_ticket.assigned_agent_id
        == agent.id
    )

def test_auto_reassignment_is_idempotent(
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

    db.refresh(
        overdue_ticket
    )

    first_assignee_id = (
        overdue_ticket.assigned_agent_id
    )

    process_sla_escalations(
        db,
        now=(
            now + timedelta(minutes=5)
        ),
    )

    db.refresh(
        overdue_ticket
    )

    assert (
        overdue_ticket.assigned_agent_id
        == first_assignee_id
    )

    assert (
        overdue_ticket.status
        == TicketStatus.ESCALATED.value
    )

    assert (
        overdue_ticket.is_escalated
        is True
    )

def test_auto_reassignment_creates_audit_event(
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

    audit_events = db.scalars(
        select(TicketAudit).where(
            TicketAudit.ticket_id
            == overdue_ticket.id
        )
    ).all()

    event_types = {
        event.event_type
        for event in audit_events
    }

    assert (
        AuditEventType.SLA_ESCALATED.value
        in event_types
    )

    assert (
        AuditEventType.TICKET_REASSIGNED.value
        in event_types
    )

def test_auto_reassignment_notifies_old_and_new_agent(
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

    reassignment_notifications = [
        notification
        for notification in notifications
        if (
            notification.type
            == NotificationType.TICKET_REASSIGNED.value
        )
    ]

    notified_user_ids = {
        notification.user_id
        for notification
        in reassignment_notifications
    }

    assert agent.id in notified_user_ids
    assert agent_two.id in notified_user_ids