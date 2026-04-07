"""
WebSocket connection manager para actualizaciones en tiempo real.
"""
from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Gestiona conexiones WebSocket activas."""

    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """Acepta y registra una nueva conexión WebSocket."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("WebSocket conectado. Conexiones activas: %d", len(self.active_connections))

    def disconnect(self, websocket: WebSocket) -> None:
        """Elimina una conexión WebSocket cerrada."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info("WebSocket desconectado. Conexiones activas: %d", len(self.active_connections))

    async def broadcast(self, message: dict[str, Any]) -> None:
        """Envía un mensaje a todas las conexiones activas."""
        payload = json.dumps(message, default=str)
        disconnected: list[WebSocket] = []
        for connection in self.active_connections:
            try:
                await connection.send_text(payload)
            except Exception:
                logger.warning("Error al enviar broadcast a conexión WebSocket", exc_info=True)
                disconnected.append(connection)
        for conn in disconnected:
            self.disconnect(conn)

    async def send_personal_message(self, message: dict[str, Any], websocket: WebSocket) -> None:
        """Envía un mensaje a una conexión específica."""
        payload = json.dumps(message, default=str)
        try:
            await websocket.send_text(payload)
        except Exception:
            logger.warning("Error al enviar mensaje personal WebSocket", exc_info=True)
            self.disconnect(websocket)
