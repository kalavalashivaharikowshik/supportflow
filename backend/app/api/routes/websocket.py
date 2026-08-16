from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    WebSocket,
)
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.websocket_service import (
    authenticate_websocket_user,
    close_unauthorized_websocket,
)
from app.websocket.manager import manager

router = APIRouter(
    tags=["WebSocket"],
)


@router.websocket(
    "/ws/notifications"
)
async def notification_websocket(
    websocket: WebSocket,
    db: Annotated[
        Session,
        Depends(get_db),
    ],
):
    token = websocket.query_params.get(
        "token"
    )

    if not token:
        await close_unauthorized_websocket(
            websocket
        )
        return

    user = authenticate_websocket_user(
        db,
        token,
    )

    if user is None:
        await close_unauthorized_websocket(
            websocket
        )
        return

    await manager.connect(
        user.id,
        websocket,
    )

    try:
        await websocket.send_json(
            {
                "type": "CONNECTED",
                "message": (
                    "WebSocket connection established."
                ),
            }
        )

        while True:
            message = (
                await websocket.receive_text()
            )

            if message == "PING":
                await websocket.send_json(
                    {
                        "type": "PONG",
                    }
                )

    except WebSocketDisconnect:
        await manager.disconnect(
            user.id,
            websocket,
        )

    except Exception:
        await manager.disconnect(
            user.id,
            websocket,
        )

        try:
            await websocket.close()

        except Exception:
            pass