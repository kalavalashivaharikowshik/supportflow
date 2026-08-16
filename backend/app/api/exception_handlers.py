import logging

from fastapi import (
    HTTPException,
    Request,
)
from fastapi.encoders import (
    jsonable_encoder,
)
from fastapi.exceptions import (
    RequestValidationError,
)
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AppException,
)

logger = logging.getLogger(
    "supportflow.error"
)


def get_request_id(
    request: Request,
) -> str | None:
    return getattr(
        request.state,
        "request_id",
        None,
    )


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "code": exc.code,
            "message": exc.message,
            "request_id": (
                get_request_id(
                    request
                )
            ),
            "details": exc.details,
        },
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
    }

    message = (
        exc.detail
        if isinstance(
            exc.detail,
            str,
        )
        else "Request failed."
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "code": code_map.get(
                exc.status_code,
                "HTTP_ERROR",
            ),
            "message": message,
            "request_id": (
                get_request_id(
                    request
                )
            ),
            "details": (
                exc.detail
                if not isinstance(
                    exc.detail,
                    str,
                )
                else None
            ),
        },
        headers=exc.headers,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    details = jsonable_encoder(
        exc.errors(),
        custom_encoder={
            ValueError: str,
        },
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "code": "VALIDATION_ERROR",
            "message": (
                "Request validation failed."
            ),
            "request_id": (
                get_request_id(
                    request
                )
            ),
            "details": details,
        },
    )

async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    request_id = get_request_id(
        request
    )

    logger.exception(
        (
            "unhandled_exception "
            "request_id=%s path=%s"
        ),
        request_id,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "code": "INTERNAL_SERVER_ERROR",
            "message": (
                "An unexpected server error occurred."
            ),
            "request_id": request_id,
            "details": None,
        },
    )