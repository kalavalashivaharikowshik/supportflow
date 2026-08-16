from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    success: bool = False
    code: str
    message: str
    request_id: str | None = None
    details: Any | None = None