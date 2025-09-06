from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any
import json

app = FastAPI()
templates = Jinja2Templates(directory="src/dashboard/templates")

# In-memory store for logs (for demonstration purposes)
log_store: List[Dict[str, Any]] = []

# WebSocket connections for real-time updates
active_connections: List[WebSocket] = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "logs": log_store})

@app.post("/log")
async def receive_log(log_entry: Dict[str, Any]):
    log_store.append(log_entry)
    # Send update to all connected WebSocket clients
    for connection in active_connections:
        await connection.send_text(json.dumps(log_entry))
    return {"message": "Log received"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keep connection alive, or handle messages if needed
            await websocket.receive_text() 
    except WebSocketDisconnect:
        active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    print("\nProject Genesis Dashboard starting...")
    print("Access dashboard at: http://localhost:8001")
    print("Log API endpoint: http://localhost:8001/log (POST)")
    uvicorn.run(app, host="0.0.0.0", port=8001)
