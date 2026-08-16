import logging

from app.db.database import SessionLocal
from app.services.escalation_service import (
    process_sla_escalations,
    process_sla_warnings,
)

logger = logging.getLogger(
    __name__
)


def run_sla_escalation_job() -> None:
    db = SessionLocal()

    try:
        warned_tickets = (
            process_sla_warnings(
                db
            )
        )

        if warned_tickets:
            logger.info(
                "SLA warning job flagged %s ticket(s).",
                len(warned_tickets),
            )
        escalated_tickets = (
            process_sla_escalations(
                db
            )
        )

        if escalated_tickets:
            logger.info(
                "SLA escalation job escalated %s ticket(s).",
                len(escalated_tickets),
            )

    except Exception:
        logger.exception(
            "SLA escalation job failed."
        )

    finally:
        db.close()