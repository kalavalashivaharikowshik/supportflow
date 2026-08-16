import time
from collections import defaultdict


class SimpleRateLimiter:
    def __init__(
        self,
        *,
        max_attempts: int,
        window_seconds: int,
    ) -> None:
        self.max_attempts = (
            max_attempts
        )

        self.window_seconds = (
            window_seconds
        )

        self.attempts: dict[
            str,
            list[float],
        ] = defaultdict(list)

    def is_allowed(
        self,
        key: str,
    ) -> bool:
        now = time.time()

        cutoff = (
            now
            - self.window_seconds
        )

        recent = [
            timestamp
            for timestamp
            in self.attempts[key]
            if timestamp >= cutoff
        ]

        self.attempts[key] = recent

        return (
            len(recent)
            < self.max_attempts
        )

    def record_attempt(
        self,
        key: str,
    ) -> None:
        self.attempts[key].append(
            time.time()
        )

    def reset(
        self,
        key: str,
    ) -> None:
        self.attempts.pop(
            key,
            None,
        )


login_rate_limiter = (
    SimpleRateLimiter(
        max_attempts=5,
        window_seconds=300,
    )
)

otp_rate_limiter = (
    SimpleRateLimiter(
        max_attempts=5,
        window_seconds=300,
    )
)