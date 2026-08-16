from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket_audit import TicketAudit


def create_audit_entry(
    db: Session,
    audit: TicketAudit,
) -> TicketAudit:
    db.add(audit)
    db.commit()
    db.refresh(audit)

    return audit


def list_ticket_audits(
    db: Session,
    *,
    ticket_id: int,
    include_internal: bool,
) -> list[TicketAudit]:
    filters = [
        TicketAudit.ticket_id == ticket_id
    ]

    if not include_internal:
        filters.append(
            TicketAudit.is_internal.is_(False)
        )

    statement = (
        select(TicketAudit)
        .where(*filters)
        .order_by(
            TicketAudit.created_at.asc()
        )
    )

    return list(
        db.scalars(statement).all()
    )