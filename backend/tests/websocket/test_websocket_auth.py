from fastapi.testclient import TestClient


def test_websocket_connects_with_valid_token(
    client: TestClient,
    agent_token: str,
):
    with client.websocket_connect(
        (
            "/ws/notifications"
            f"?token={agent_token}"
        )
    ) as websocket:
        message = websocket.receive_json()

        assert (
            message["type"]
            == "CONNECTED"
        )