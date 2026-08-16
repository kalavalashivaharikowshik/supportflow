from apscheduler.schedulers.background import (
    BackgroundScheduler,
)

from app.db.database import SessionLocal
from app.scheduler.jobs import (
    run_sla_escalation_job,
)
from app.services.app_config_service import (
    get_or_create_app_config,
)

scheduler = BackgroundScheduler(
    timezone="UTC",
)


def start_scheduler() -> None:
    if scheduler.running:
        return

    db = SessionLocal()

    try:
        config = get_or_create_app_config(
            db
        )

        interval_seconds = (
            config.escalation_check_interval_seconds
        )

    finally:
        db.close()

    scheduler.add_job(
        run_sla_escalation_job,
        trigger="interval",
        seconds=interval_seconds,
        id="sla_escalation_job",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()


def update_sla_job_interval(
    seconds: int,
) -> None:
    if not scheduler.running:
        return

    scheduler.reschedule_job(
        "sla_escalation_job",
        trigger="interval",
        seconds=seconds,
    )


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(
            wait=False
        )