from fastapi import FastAPI

from src.api.genesis import router as genesis_router

app = FastAPI()

app.include_router(genesis_router, prefix="/genesis", tags=["genesis"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to Project Genesis - AI-Native Development Platform"}

# Placeholder for future AI agent orchestration and natural language processing

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)