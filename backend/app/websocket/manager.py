import asyncio

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[
            int,
            set[WebSocket],
        ] = {}

        self._lock = asyncio.Lock()
        self.event_loop: (
            asyncio.AbstractEventLoop | None
        ) = None

    async def connect(
        self,
        user_id: int,
        websocket: WebSocket,
    ) -> None:
        self.event_loop = (
            asyncio.get_running_loop()
        )
        await websocket.accept()

        async with self._lock:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = set()

            self.active_connections[user_id].add(
                websocket
            )

    async def disconnect(
        self,
        user_id: int,
        websocket: WebSocket,
    ) -> None:
        async with self._lock:
            connections = (
                self.active_connections.get(
                    user_id
                )
            )

            if not connections:
                return

            connections.discard(
                websocket
            )

            if not connections:
                self.active_connections.pop(
                    user_id,
                    None,
                )

    async def send_to_user(
        self,
        user_id: int,
        payload: dict,
    ) -> None:
        async with self._lock:
            connections = list(
                self.active_connections.get(
                    user_id,
                    set(),
                )
            )

        disconnected: list[WebSocket] = []

        for websocket in connections:
            try:
                await websocket.send_json(
                    payload
                )

            except Exception:
                disconnected.append(
                    websocket
                )

        for websocket in disconnected:
            await self.disconnect(
                user_id,
                websocket,
            )

    def is_connected(
        self,
        user_id: int,
    ) -> bool:
        connections = (
            self.active_connections.get(
                user_id
            )
        )

        return bool(connections)


manager = ConnectionManager()