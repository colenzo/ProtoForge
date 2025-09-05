from fastapi import APIRouter
from pydantic import BaseModel

from src.agents.code_generator import generate_code, CodeGenerationInput, GeneratedCode
from src.agents.testing_agent import run_tests, TestingInput, TestingOutput
from src.models.genesis_response import GenesisResponse

router = APIRouter()

class IdeaInput(BaseModel):
    idea: str

@router.post("/idea", response_model=GenesisResponse)
async def process_idea(idea_input: IdeaInput):
    """Receives a natural language idea and initiates the project genesis process."""
    print(f"Received idea: {idea_input.idea}")
    
    # Trigger code generation
    code_gen_input = CodeGenerationInput(idea=idea_input.idea)
    generated_code = await generate_code(code_gen_input)
    
    # Trigger automated testing
    testing_input = TestingInput(code=generated_code.code)
    testing_results = await run_tests(testing_input)
    
    return GenesisResponse(
        idea=idea_input.idea,
        generated_code=generated_code,
        testing_results=testing_results
    )
