from fastapi.websockets import WebSocket
from datetime import datetime


class websocket_manager:
    def __init__(self):
        # Simple list to store connected clients
        self.connected_clients = []

    async def connect(self, websocket: WebSocket):
        """When a new client connects"""
        # Accept the WebSocket connection
        await websocket.accept()
        
        # Add client to our list
        self.connected_clients.append(websocket)
        
        # Get client info for logging
        client_info = f"{websocket.client.host}:{websocket.client.port}"
        print(f"✅ New client connected: {client_info}")
        print(f"📊 Total connected clients: {len(self.connected_clients)}")
        
        # Send welcome message to the new client only
        welcome_message = {
            "type": "system",
            "client": "Server",
            "message": "Welcome to the chat!",
            "timestamp": self.get_current_time()
        }
        await websocket.send_json(welcome_message)
        
        # Tell other clients someone joined
        if len(self.connected_clients) > 1:  # Only if there are other clients
            join_message = {
                "type": "notification", 
                "message": f"User {client_info} joined the chat",
                "timestamp": self.get_current_time()
            }
            await self.send_to_others(websocket, join_message)

    async def send_message(self, sender_websocket: WebSocket, message: dict):
        """When a client sends a message, broadcast it to others"""
        # Get sender info
        sender_info = f"{sender_websocket.client.host}:{sender_websocket.client.port}"
        
        # Create the message to send to other clients
        broadcast_message = {
            "type": "message",
            "client": sender_info,
            "content": message.get("content", ""),
            "timestamp": self.get_current_time()
        }
        
        print(f"📤 Broadcasting message from {sender_info}: {message.get('content', '')}")
        
        # Send to all other clients (not the sender)
        await self.send_to_others(sender_websocket, broadcast_message)

    async def send_to_others(self, sender_websocket: WebSocket, message: dict):
        """Send message to all clients except the sender"""
        # Go through each connected client
        clients_to_remove = []
        
        for client in self.connected_clients:
            # Skip the sender
            if client == sender_websocket:
                continue
                
            try:
                # Try to send the message
                await client.send_json(message)
            except:
                # If sending fails, mark client for removal
                print(f"❌ Failed to send to client, will remove them")
                clients_to_remove.append(client)
        
        # Remove clients that failed
        for client in clients_to_remove:
            await self.disconnect(client)

    async def disconnect(self, websocket: WebSocket):
        """When a client disconnects"""
        # Get client info
        client_info = f"{websocket.client.host}:{websocket.client.port}"
        
        # Remove from our list (only if still in the list)
        if websocket in self.connected_clients:
            self.connected_clients.remove(websocket)
            print(f"❌ Client disconnected: {client_info}")
            print(f"📊 Total connected clients: {len(self.connected_clients)}")
            
            # Tell remaining clients someone left (but don't call disconnect again)
            if self.connected_clients:  # Only if there are still clients
                leave_message = {
                    "type": "notification",
                    "message": f"User {client_info} left the chat", 
                    "timestamp": self.get_current_time()
                }
                # Send directly without calling disconnect on failures
                await self.send_notification_only(leave_message)

    async def send_notification_only(self, message: dict):
        """Send notification without handling disconnections to avoid loops"""
        for client in self.connected_clients:
            try:
                await client.send_json(message)
            except:
                # Just log the error, don't try to disconnect (to avoid loops)
                print(f"⚠️ Failed to send notification to a client")

    async def send_to_all(self, message: dict):
        """Send message to ALL connected clients"""
        clients_to_remove = []
        
        for client in self.connected_clients:
            try:
                await client.send_json(message)
            except:
                print(f"❌ Failed to send to client, will remove them")
                clients_to_remove.append(client)
        
        # Remove failed clients
        for client in clients_to_remove:
            await self.disconnect(client)

    def get_current_time(self):
        """Get current time as a string"""
        return datetime.now().isoformat()

    def get_connected_count(self):
        """Get number of connected clients"""
        return len(self.connected_clients)
    