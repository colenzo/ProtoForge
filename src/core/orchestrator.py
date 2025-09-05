from src.agents.code_generator import generate_code, CodeGenerationInput, GeneratedCode
from src.agents.testing_agent import run_tests, TestingInput, TestingOutput
from src.agents.deployment_agent import deploy_application, DeploymentInput, DeploymentOutput
from src.agents.security_agent import run_security_scan, SecurityReport
from src.agents.integration_agent import integrate_external_service, IntegrationInput, IntegrationResult
from src.agents.infrastructure_agent import generate_infrastructure_code, InfrastructureInput, InfrastructureOutput
from src.models.genesis_response import GenesisResponse
from src.core.knowledge_logger import log_to_knowledge_vault
from src.core.nexus_manager import perform_nexus_check

async def orchestrate_genesis_process(idea: str) -> GenesisResponse:
    """Orchestrates the end-to-end Project Genesis process from idea to deployment."""
    
    security_report = None
    infrastructure_results = None
    testing_results = None
    deployment_results = None
    integration_results = None

    # 1. Code Generation
    await perform_nexus_check("Code Generation", "start")
    code_gen_input = CodeGenerationInput(idea=idea)
    generated_code = await generate_code(code_gen_input)
    await log_to_knowledge_vault("code_generation_completed", {"idea": idea, "status": generated_code.status, "message": generated_code.message})
    
    if generated_code.status == "failure":
        return GenesisResponse(
            idea=idea,
            generated_code=generated_code,
            security_report=security_report,
            infrastructure_results=infrastructure_results,
            testing_results=testing_results,
            deployment_results=deployment_results,
            integration_results=integration_results
        )

    # 2. Security Scan (Aegis Protocol)
    await perform_nexus_check("Security Scan", "start")
    security_report = await run_security_scan(generated_code.code)
    await log_to_knowledge_vault("security_scan_completed", {"idea": idea, "status": security_report.status, "findings_count": len(security_report.findings)})
    
    if security_report.status == "failed":
        return GenesisResponse(
            idea=idea,
            generated_code=generated_code,
            security_report=security_report,
            infrastructure_results=infrastructure_results,
            testing_results=testing_results,
            deployment_results=deployment_results,
            integration_results=integration_results
        )

    # 3. Infrastructure Generation (Terraform Protocol)
    await perform_nexus_check("Infrastructure Generation", "start")
    # Assuming a summary of the generated code is enough for basic IaC generation
    infrastructure_input = InfrastructureInput(application_code_summary=generated_code.code[:200]) # Pass a summary
    infrastructure_results = await generate_infrastructure_code(infrastructure_input)
    await log_to_knowledge_vault("infrastructure_generation_completed", {"idea": idea, "status": infrastructure_results.status, "iac_code_summary": infrastructure_results.iac_code[:100]})
    
    if infrastructure_results.status == "failed":
        return GenesisResponse(
            idea=idea,
            generated_code=generated_code,
            security_report=security_report,
            infrastructure_results=infrastructure_results,
            testing_results=testing_results,
            deployment_results=deployment_results,
            integration_results=integration_results
        )

    # 4. Automated Testing
    await perform_nexus_check("Automated Testing", "start")
    testing_input = TestingInput(code=generated_code.code)
    testing_results = await run_tests(testing_input)
    await log_to_knowledge_vault("testing_completed", {"idea": idea, "overall_status": testing_results.status, "test_results_summary": [r.status for r in testing_results.test_results]})
    
    if testing_results.status == "failure":
        return GenesisResponse(
            idea=idea,
            generated_code=generated_code,
            security_report=security_report,
            infrastructure_results=infrastructure_results,
            testing_results=testing_results,
            deployment_results=deployment_results,
            integration_results=integration_results
        )

    # 5. Automated Deployment
    await perform_nexus_check("Automated Deployment", "start")
    deployment_input = DeploymentInput(code=generated_code.code, test_status=testing_results.status)
    deployment_results = await deploy_application(deployment_input)
    await log_to_knowledge_vault("deployment_completed", {"idea": idea, "status": deployment_results.status, "url": deployment_results.deployment_url})
    
    if deployment_results.status == "failure":
        return GenesisResponse(
            idea=idea,
            generated_code=generated_code,
            security_report=security_report,
            infrastructure_results=infrastructure_results,
            testing_results=testing_results,
            deployment_results=deployment_results,
            integration_results=integration_results
        )

    # 6. External Service Integration (Meridian Protocol)
    await perform_nexus_check("External Service Integration", "start")
    # For demonstration, let's assume we integrate a dummy analytics service
    integration_input = IntegrationInput(service_name="Dummy Analytics", api_endpoint="https://api.dummy-analytics.com")
    integration_results = await integrate_external_service(integration_input)
    await log_to_knowledge_vault("integration_completed", {"idea": idea, "service": integration_input.service_name, "status": integration_results.status})
    
    return GenesisResponse(
        idea=idea,
        generated_code=generated_code,
        security_report=security_report,
        infrastructure_results=infrastructure_results,
        testing_results=testing_results,
        deployment_results=deployment_results,
        integration_results=integration_results
    )
