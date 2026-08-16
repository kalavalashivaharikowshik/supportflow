from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.api.exception_handlers import (
    app_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.api.middleware.request_context import (
    RequestContextMiddleware,
)
from app.api.middleware.request_logging import (
    RequestLoggingMiddleware,
)
from app.api.middleware.security_headers import (
    SecurityHeadersMiddleware,
)
from app.api.router import api_router
from app.api.routes import websocket
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.logging import configure_logging
from app.scheduler.scheduler import (
    start_scheduler,
    stop_scheduler,
)

configure_logging(
    settings.log_level
)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    del app

    if not settings.testing:
        start_scheduler()

    yield

    if not settings.testing:
        stop_scheduler()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "SupportFlow - SLA-Driven Support Ticket "
        "Escalation System API"
    ),
    lifespan=lifespan,
)


# ---------------------------------
# Exception Handlers
# ---------------------------------

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)


# ---------------------------------
# CORS
# ---------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        settings.cors_origin_list
    ),
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Request-ID",
    ],
    expose_headers=[
        "X-Request-ID",
    ],
)


# ---------------------------------
# Trusted Hosts
# ---------------------------------

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=(
        settings.allowed_host_list
    ),
)


# ---------------------------------
# Security / Logging / Request ID
# ---------------------------------

app.add_middleware(
    SecurityHeadersMiddleware,
)

app.add_middleware(
    RequestLoggingMiddleware,
)

app.add_middleware(
    RequestContextMiddleware,
)


# ---------------------------------
# Routers
# ---------------------------------

app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    websocket.router,
)


# ---------------------------------
# Root
# ---------------------------------

@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "message": "SupportFlow API is running",
        "docs": "/docs",
        "health": (
            f"{settings.api_v1_prefix}/health"
        ),
    }