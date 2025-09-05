from fastapi import APIRouter
from pydantic import BaseModel

from src.agents.code_generator import generate_code, CodeGenerationInput, GeneratedCode

router = APIRouter()

class IdeaInput(BaseModel):
    idea: str

@router.post("/idea", response_model=GeneratedCode)
async def process_idea(idea_input: IdeaInput):
    """Receives a natural language idea and initiates the project genesis process."""
    # Placeholder for actual AI processing and project initiation
    print(f"Received idea: {idea_input.idea}")
    
    # Trigger code generation
    code_gen_input = CodeGenerationInput(idea=idea_input.idea)
    generated_code = await generate_code(code_gen_input)
    
    return generated_code
