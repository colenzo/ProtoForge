from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class IdeaInput(BaseModel):
    idea: str

@router.post("/idea")
async def process_idea(idea_input: IdeaInput):
    """Receives a natural language idea and initiates the project genesis process."""
    # Placeholder for actual AI processing and project initiation
    print(f"Received idea: {idea_input.idea}")
    return {"message": "Idea received, initiating Project Genesis process...", "idea": idea_input.idea}
