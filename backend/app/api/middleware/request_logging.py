import logging
import time

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.responses import Response

logger = logging.getLogger(
    "supportflow.request"
)


class RequestLoggingMiddleware(
    BaseHTTPMiddleware
):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start_time = time.perf_counter()

        try:
            response = await call_next(
                request
            )

        except Exception:
            duration_ms = (
                time.perf_counter()
                - start_time
            ) * 1000

            request_id = getattr(
                request.state,
                "request_id",
                "unknown",
            )

            logger.exception(
                (
                    "request_failed "
                    "request_id=%s method=%s "
                    "path=%s duration_ms=%.2f"
                ),
                request_id,
                request.method,
                request.url.path,
                duration_ms,
            )

            raise

        duration_ms = (
            time.perf_counter()
            - start_time
        ) * 1000

        request_id = getattr(
            request.state,
            "request_id",
            "unknown",
        )

        logger.info(
            (
                "request_completed "
                "request_id=%s method=%s "
                "path=%s status=%s "
                "duration_ms=%.2f"
            ),
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response