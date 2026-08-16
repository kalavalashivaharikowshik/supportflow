from datetime import datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.permissions import (
    require_admin,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.common import (
    AgentPerformanceReportItem,
    SLAReportItem,
    TicketReportSummary,
)
from app.services.report_service import (
    export_agent_performance_csv,
    export_sla_report_csv,
    export_ticket_report_csv,
    get_agent_performance_report,
    get_sla_breach_report,
    get_ticket_report_summary,
)


def validate_date_range(
    start_date: datetime | None,
    end_date: datetime | None,
) -> None:
    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "start_date must be earlier "
                "than or equal to end_date."
            ),
        )

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

@router.get(
    "/tickets/summary",
    response_model=TicketReportSummary,
)
def ticket_summary(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
    start_date: datetime | None = Query(
        default=None,
    ),
    end_date: datetime | None = Query(
        default=None,
    ),
):
    del admin

    validate_date_range(
        start_date,
        end_date,
    )

    return get_ticket_report_summary(
        db,
        start_date=start_date,
        end_date=end_date,
    )

@router.get(
    "/sla-breaches",
    response_model=list[SLAReportItem],
)
def sla_breach_report(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
    start_date: datetime | None = Query(
        default=None,
    ),
    end_date: datetime | None = Query(
        default=None,
    ),
):
    del admin

    validate_date_range(
        start_date,
        end_date,
    )

    return get_sla_breach_report(
        db,
        start_date=start_date,
        end_date=end_date,
    )

@router.get(
    "/agents/performance",
    response_model=list[
        AgentPerformanceReportItem
    ],
)
def agent_performance_report(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
    start_date: datetime | None = Query(
        default=None,
    ),
    end_date: datetime | None = Query(
        default=None,
    ),
):
    del admin

    validate_date_range(
        start_date,
        end_date,
    )

    return get_agent_performance_report(
        db,
        start_date=start_date,
        end_date=end_date,
    )
def csv_response(
    *,
    content: str,
    filename: str,
) -> Response:
    return Response(
        content=content,
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            ),
        },
    )

@router.get(
    "/tickets/export",
)
def export_tickets(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
    start_date: datetime | None = Query(
        default=None,
    ),
    end_date: datetime | None = Query(
        default=None,
    ),
):
    del admin

    validate_date_range(
        start_date,
        end_date,
    )

    content = export_ticket_report_csv(
        db,
        start_date=start_date,
        end_date=end_date,
    )

    return csv_response(
        content=content,
        filename="supportflow-tickets.csv",
    )

@router.get(
    "/sla-breaches/export",
)
def export_sla_breaches(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
    start_date: datetime | None = Query(
        default=None,
    ),
    end_date: datetime | None = Query(
        default=None,
    ),
):
    del admin

    validate_date_range(
        start_date,
        end_date,
    )

    content = export_sla_report_csv(
        db,
        start_date=start_date,
        end_date=end_date,
    )

    return csv_response(
        content=content,
        filename=(
            "supportflow-sla-breaches.csv"
        ),
    )

@router.get(
    "/agents/performance/export",
)
def export_agent_performance(
    db: Annotated[
        Session,
        Depends(get_db),
    ],
    admin: Annotated[
        User,
        Depends(require_admin),
    ],
    start_date: datetime | None = Query(
        default=None,
    ),
    end_date: datetime | None = Query(
        default=None,
    ),
):
    del admin

    validate_date_range(
        start_date,
        end_date,
    )

    content = (
        export_agent_performance_csv(
            db,
            start_date=start_date,
            end_date=end_date,
        )
    )

    return csv_response(
        content=content,
        filename=(
            "supportflow-agent-performance.csv"
        ),
    )