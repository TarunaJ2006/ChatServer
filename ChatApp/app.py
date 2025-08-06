from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.websockets import WebSocket, WebSocketDisconnect
from manager import websocket_manager


app = FastAPI()


manager = websocket_manager()

templates = Jinja2Templates(
    directory="Templates"
    )

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/stats")
async def get_stats():
    """Get server statistics"""
    return {
        "connected_clients": manager.get_connected_count(),
        "status": "running"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_json()
            print(f"Received message: {message}")
            await manager.send_message(websocket, message)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        print(f"Error in websocket connection: {e}")
        await manager.disconnect(websocket)