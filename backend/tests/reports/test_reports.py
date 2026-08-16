from fastapi.testclient import TestClient

from tests.helpers import auth_headers


def test_admin_can_access_ticket_summary_report(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        "/api/reports/tickets/summary",
        headers=auth_headers(
            admin_token
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert "total_tickets" in body
    assert "active_tickets" in body
    assert "resolved_tickets" in body
    assert "closed_tickets" in body
    assert "escalated_tickets" in body
    assert "sla_breached_tickets" in body


def test_requester_cannot_access_ticket_summary_report(
    client: TestClient,
    requester_token: str,
):
    response = client.get(
        "/api/reports/tickets/summary",
        headers=auth_headers(
            requester_token
        ),
    )

    assert response.status_code == 403


def test_invalid_report_date_range_returns_400(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        (
            "/api/reports/tickets/summary"
            "?start_date=2026-08-20T00:00:00Z"
            "&end_date=2026-08-10T00:00:00Z"
        ),
        headers=auth_headers(
            admin_token
        ),
    )

    assert response.status_code == 400

    body = response.json()

    assert body["success"] is False
    assert body["code"] == "BAD_REQUEST"

    assert (
        body["message"]
        == (
            "start_date must be earlier "
            "than or equal to end_date."
        )
    )


def test_ticket_csv_export_returns_csv(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        "/api/reports/tickets/export",
        headers=auth_headers(
            admin_token
        ),
    )

    assert response.status_code == 200

    content_type = response.headers.get(
        "content-type"
    )

    assert content_type is not None
    assert "text/csv" in content_type


def test_ticket_csv_export_has_attachment_header(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        "/api/reports/tickets/export",
        headers=auth_headers(
            admin_token
        ),
    )

    assert response.status_code == 200

    disposition = response.headers.get(
        "content-disposition"
    )

    assert disposition is not None

    assert (
        'filename="supportflow-tickets.csv"'
        in disposition
    )


def test_requester_cannot_export_ticket_report(
    client: TestClient,
    requester_token: str,
):
    response = client.get(
        "/api/reports/tickets/export",
        headers=auth_headers(
            requester_token
        ),
    )

    assert response.status_code == 403


def test_reports_without_authentication_return_401(
    client: TestClient,
):
    response = client.get(
        "/api/reports/tickets/summary"
    )

    assert response.status_code == 401