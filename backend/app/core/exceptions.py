from typing import Any


class AppException(Exception):
    def __init__(
        self,
        *,
        status_code: int,
        code: str,
        message: str,
        details: Any | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details

        super().__init__(message)


class NotFoundException(AppException):
    def __init__(
        self,
        *,
        code: str,
        message: str,
    ) -> None:
        super().__init__(
            status_code=404,
            code=code,
            message=message,
        )


class ForbiddenException(AppException):
    def __init__(
        self,
        *,
        code: str,
        message: str,
    ) -> None:
        super().__init__(
            status_code=403,
            code=code,
            message=message,
        )


class ConflictException(AppException):
    def __init__(
        self,
        *,
        code: str,
        message: str,
    ) -> None:
        super().__init__(
            status_code=409,
            code=code,
            message=message,
        )


class BadRequestException(AppException):
    def __init__(
        self,
        *,
        code: str,
        message: str,
    ) -> None:
        super().__init__(
            status_code=400,
            code=code,
            message=message,
        )

class RateLimitException(
    AppException
):
    def __init__(
        self,
        *,
        message: str = (
            "Too many requests. "
            "Please try again later."
        ),
    ) -> None:
        super().__init__(
            status_code=429,
            code="RATE_LIMITED",
            message=message,
        )