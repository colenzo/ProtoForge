from fastapi import FastAPI
import asyncio

from src.api.genesis import router as genesis_router
from src.core.lumen_analyzer import run_lumen_feedback_loop

app = FastAPI()

app.include_router(genesis_router, prefix="/genesis", tags=["genesis"])

@app.on_event("startup")
async def startup_event():
    print("Starting Lumen feedback loop in background...")
    asyncio.create_task(run_lumen_feedback_loop())

@app.get("/")
async def read_root():
    return {"message": "Welcome to Project Genesis - AI-Native Development Platform"}

# Placeholder for future AI agent orchestration and natural language processing

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
