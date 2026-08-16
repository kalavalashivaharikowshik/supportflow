from datetime import datetime, timezone


def generate_ticket_number(
    ticket_id: int,
) -> str:
    year = datetime.now(
        timezone.utc
    ).year

    return f"SUP-{year}-{ticket_id:06d}"