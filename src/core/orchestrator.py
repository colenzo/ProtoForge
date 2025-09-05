from src.agents.code_generator import generate_code, CodeGenerationInput, GeneratedCode
from src.agents.testing_agent import run_tests, TestingInput, TestingOutput
from src.agents.deployment_agent import deploy_application, DeploymentInput, DeploymentOutput
from src.models.genesis_response import GenesisResponse

async def orchestrate_genesis_process(idea: str) -> GenesisResponse:
    """Orchestrates the end-to-end Project Genesis process from idea to deployment."""
    
    # 1. Code Generation
    code_gen_input = CodeGenerationInput(idea=idea)
    generated_code = await generate_code(code_gen_input)
    
    # 2. Automated Testing
    testing_input = TestingInput(code=generated_code.code)
    testing_results = await run_tests(testing_input)
    
    # 3. Automated Deployment
    deployment_input = DeploymentInput(code=generated_code.code, test_status=testing_results.status)
    deployment_results = await deploy_application(deployment_input)
    
    return GenesisResponse(
        idea=idea,
        generated_code=generated_code,
        testing_results=testing_results,
        deployment_results=deployment_results
    )
