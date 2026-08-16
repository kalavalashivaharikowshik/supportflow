from fastapi import APIRouter

from app.api.routes import (
    app_config,
    auth,
    dashboard,
    health,
    notifications,
    reports,
    sla,
    ticket_audit,
    ticket_responses,
    tickets,
    users,
)

api_router = APIRouter()

api_router.include_router(
    health.router,
)

api_router.include_router(
    auth.router,
)

api_router.include_router(
    users.router,
)

api_router.include_router(
    tickets.router,
)

api_router.include_router(
    ticket_responses.router,
)

api_router.include_router(
    sla.router,
)

api_router.include_router(
    ticket_audit.router,
)

api_router.include_router(
    notifications.router,
)

api_router.include_router(
    dashboard.router,
)

api_router.include_router(
    reports.router,
)

api_router.include_router(
    app_config.router,
)