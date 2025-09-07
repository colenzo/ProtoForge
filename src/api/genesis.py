from fastapi import APIRouter
from pydantic import BaseModel

from src.models.genesis_response import GenesisResponse
from src.core.orchestrator import orchestrate_genesis_process

router = APIRouter()

class IdeaInput(BaseModel):
    idea: str

@router.post("/idea", response_model=GenesisResponse)
async def process_idea(idea_input: IdeaInput):
    """Receives a natural language idea and initiates the project genesis process."""
    print(f"Received idea: {idea_input.idea}")
    
    # Orchestrate the entire genesis process
    response = await orchestrate_genesis_process(idea_input.idea)
    
    return response

@router.get("/test")
async def test_route():
    return {"message": "test route works"}
