from fastapi.websockets import WebSocket
from datetime import datetime


class websocket_manager:
    """Simple WebSocket connection manager expected by `app.py` (instantiated as `websocket_manager()`)."""

    def __init__(self):
        self.connected_clients = []  # type: list[WebSocket]

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connected_clients.append(websocket)

        client_info = f"{websocket.client.host}:{websocket.client.port}"
        print(f"✅ New client connected: {client_info}")
        print(f"📊 Total connected clients: {len(self.connected_clients)}")

        welcome_message = {
            "type": "system",
            "client": "Server",
            "message": "Welcome to the chat!",
            "timestamp": self.get_current_time(),
        }
        await websocket.send_json(welcome_message)

        if len(self.connected_clients) > 1:
            join_message = {
                "type": "notification",
                "message": f"User {client_info} joined the chat",
                "timestamp": self.get_current_time(),
            }
            await self.send_to_others(websocket, join_message)

    async def send_message(self, sender_websocket: WebSocket, message: dict):
        sender_info = f"{sender_websocket.client.host}:{sender_websocket.client.port}"
        broadcast_message = {
            "type": "message",
            "client": sender_info,
            "content": message.get("content", ""),
            "timestamp": self.get_current_time(),
        }
        print(f"📤 Broadcasting message from {sender_info}: {broadcast_message['content']}")
        await self.send_to_others(sender_websocket, broadcast_message)

    async def send_to_others(self, sender_websocket: WebSocket, message: dict):
        clients_to_remove = []
        for client in list(self.connected_clients):
            if client is sender_websocket:
                continue
            try:
                await client.send_json(message)
            except Exception:
                print("❌ Failed to send to client, will remove them")
                clients_to_remove.append(client)

        for client in clients_to_remove:
            await self.disconnect(client)

    async def send_to_all(self, message: dict):
        clients_to_remove = []
        for client in list(self.connected_clients):
            try:
                await client.send_json(message)
            except Exception:
                print("❌ Failed to send to client, will remove them")
                clients_to_remove.append(client)

        for client in clients_to_remove:
            await self.disconnect(client)

    async def disconnect(self, websocket: WebSocket):
        client_info = f"{websocket.client.host}:{websocket.client.port}"
        if websocket in self.connected_clients:
            try:
                self.connected_clients.remove(websocket)
            except ValueError:
                pass
            print(f"❌ Client disconnected: {client_info}")
            print(f"📊 Total connected clients: {len(self.connected_clients)}")

            if self.connected_clients:
                leave_message = {
                    "type": "notification",
                    "message": f"User {client_info} left the chat",
                    "timestamp": self.get_current_time(),
                }
                await self.send_notification_only(leave_message)

    async def send_notification_only(self, message: dict):
        for client in list(self.connected_clients):
            try:
                await client.send_json(message)
            except Exception:
                print("⚠️ Failed to send notification to a client")

    def get_current_time(self) -> str:
        return datetime.now().isoformat()

    def get_connected_count(self) -> int:
        return len(self.connected_clients)

    # PR marker: minor non-functional change to trigger pull request creation

