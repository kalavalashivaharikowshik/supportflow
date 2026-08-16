from fastapi.testclient import TestClient


def auth_headers(
    token: str,
) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
    }


def valid_config_payload(
    *,
    auto_reassign_on_escalation: bool,
) -> dict:
    return {
        "sla_warning_threshold_percent": 80,
        "escalation_check_interval_seconds": 60,
        "max_active_tickets_per_agent": 20,
        "auto_reassign_on_escalation": auto_reassign_on_escalation,
        "allow_requester_reopen": True,
        "allow_admin_public_response": True,
        "notifications_enabled": True,
        "websocket_notifications_enabled": True,
    }


def test_admin_config_returns_auto_reassignment_setting(
    client: TestClient,
    admin_token: str,
):
    response = client.get(
        "/api/admin/config",
        headers=auth_headers(admin_token),
    )

    assert response.status_code == 200

    body = response.json()

    assert "auto_reassign_on_escalation" in body
    assert body["auto_reassign_on_escalation"] is True


def test_admin_can_disable_auto_reassignment(
    client: TestClient,
    admin_token: str,
):
    response = client.put(
        "/api/admin/config",
        headers=auth_headers(admin_token),
        json=valid_config_payload(
            auto_reassign_on_escalation=False,
        ),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["auto_reassign_on_escalation"] is False

    get_response = client.get(
        "/api/admin/config",
        headers=auth_headers(admin_token),
    )

    assert get_response.status_code == 200
    assert (
        get_response.json()["auto_reassign_on_escalation"]
        is False
    )


def test_requester_cannot_update_auto_reassignment_setting(
    client: TestClient,
    requester_token: str,
):
    response = client.put(
        "/api/admin/config",
        headers=auth_headers(requester_token),
        json=valid_config_payload(
            auto_reassign_on_escalation=False,
        ),
    )

    assert response.status_code == 403