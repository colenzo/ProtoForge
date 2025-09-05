from src.agents.code_generator import generate_code, CodeGenerationInput, GeneratedCode
from src.agents.testing_agent import run_tests, TestingInput, TestingOutput
from src.agents.deployment_agent import deploy_application, DeploymentInput, DeploymentOutput
from src.models.genesis_response import GenesisResponse
from src.core.knowledge_logger import log_to_knowledge_vault

async def orchestrate_genesis_process(idea: str) -> GenesisResponse:
    """Orchestrates the end-to-end Project Genesis process from idea to deployment."""
    
    # 1. Code Generation
    code_gen_input = CodeGenerationInput(idea=idea)
    generated_code = await generate_code(code_gen_input)
    await log_to_knowledge_vault("code_generation_completed", {"idea": idea, "status": generated_code.status, "message": generated_code.message})
    
    # 2. Automated Testing
    testing_input = TestingInput(code=generated_code.code)
    testing_results = await run_tests(testing_input)
    await log_to_knowledge_vault("testing_completed", {"idea": idea, "overall_status": testing_results.status, "test_results_summary": [r.status for r in testing_results.test_results]})
    
    # 3. Automated Deployment
    deployment_input = DeploymentInput(code=generated_code.code, test_status=testing_results.status)
    deployment_results = await deploy_application(deployment_input)
    await log_to_knowledge_vault("deployment_completed", {"idea": idea, "status": deployment_results.status, "url": deployment_results.deployment_url})
    
    return GenesisResponse(
        idea=idea,
        generated_code=generated_code,
        testing_results=testing_results,
        deployment_results=deployment_results
    )
