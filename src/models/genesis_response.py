from pydantic import BaseModel
from typing import List, Optional, Dict

from src.agents.code_generator import GeneratedCode
from src.agents.testing_agent import TestingOutput, TestResult
from src.agents.deployment_agent import DeploymentOutput
from src.agents.security_agent import SecurityReport
from src.agents.integration_agent import IntegrationResult
from src.agents.infrastructure_agent import InfrastructureOutput

class GenesisResponse(BaseModel):
    idea: str
    generated_code: GeneratedCode
    testing_results: Optional[TestingOutput] = None
    deployment_results: Optional[DeploymentOutput] = None
    security_report: Optional[SecurityReport] = None
    integration_results: Optional[IntegrationResult] = None
    infrastructure_results: Optional[InfrastructureOutput] = None
    agent_instance_ids: Dict[str, int] = {} # New field for agent instance IDs
    # Potentially add more fields for deployment results, etc.
