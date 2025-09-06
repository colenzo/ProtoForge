from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any
import json
import httpx # For making HTTP requests to the main API
import os # Import os module

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates")) # Ensure absolute path

# In-memory store for logs (for demonstration purposes)
log_store: List[Dict[str, Any]] = []

# WebSocket connections for real-time updates
active_connections: List[WebSocket] = []

# Base URL for the main Project Genesis API
PROJECT_GENESIS_API_URL = "http://localhost:8000/genesis/idea"

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

@app.post("/submit_idea")
async def submit_idea(request: Request, idea: str = Form(...)):
    print(f"[DASHBOARD] Received idea from UI: {idea}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(PROJECT_GENESIS_API_URL, json={"idea": idea})
            response.raise_for_status()
            genesis_response = response.json()
            print(f"[DASHBOARD] Project Genesis API response: {json.dumps(genesis_response, indent=2)}")
            # You might want to store this full response or send it via WebSocket
            # For now, we'll just redirect back to the main page
            return RedirectResponse(url="/", status_code=303)
    except httpx.RequestError as e:
        print(f"[DASHBOARD] Error connecting to Project Genesis API: {e}")
        return HTMLResponse(content=f"<h1>Error: Could not connect to Project Genesis API. Is it running?</h1><p>{e}</p>", status_code=500)
    except httpx.HTTPStatusError as e:
        print(f"[DASHBOARD] API returned an error: {e.response.status_code} - {e.response.text}")
        return HTMLResponse(content=f"<h1>API Error: {e.response.status_code}</h1><p>{e.response.text}</p>", status_code=e.response.status_code)

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
