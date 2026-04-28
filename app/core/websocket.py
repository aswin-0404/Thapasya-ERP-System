from fastapi import WebSocket
from typing import List

class ConnectionManager:
    def __init__(self):
        # We store connections in a list, though for one admin it will usually be just one
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # Send data to all connected admins
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()