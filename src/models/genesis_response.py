from pydantic import BaseModel
from typing import List, Optional

from src.agents.code_generator import GeneratedCode
from src.agents.testing_agent import TestingOutput, TestResult
from src.agents.deployment_agent import DeploymentOutput

class GenesisResponse(BaseModel):
    idea: str
    generated_code: GeneratedCode
    testing_results: Optional[TestingOutput] = None
    deployment_results: Optional[DeploymentOutput] = None
    # Potentially add more fields for deployment results, etc.
