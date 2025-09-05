from src.agents.code_generator import generate_code, CodeGenerationInput, GeneratedCode
from src.agents.testing_agent import run_tests, TestingInput, TestingOutput
from src.agents.deployment_agent import deploy_application, DeploymentInput, DeploymentOutput
from src.agents.security_agent import run_security_scan, SecurityReport
from src.agents.integration_agent import integrate_external_service, IntegrationInput, IntegrationResult
from src.agents.infrastructure_agent import generate_infrastructure_code, InfrastructureInput, InfrastructureOutput
from src.models.genesis_response import GenesisResponse
from src.core.knowledge_logger import log_to_knowledge_vault
from src.core.nexus_manager import perform_nexus_check, NexusCheckResult

async def orchestrate_genesis_process(idea: str) -> GenesisResponse:
    """Orchestrates the end-to-end Project Genesis process from idea to deployment."""
    
    security_report = None
    infrastructure_results = None
    testing_results = None
    deployment_results = None
    integration_results = None

    async def _run_with_nexus_check(protocol_name: str, action: str, func, *args, **kwargs):
        check_result = await perform_nexus_check(protocol_name, action)
        if check_result.status == "conflict_detected":
            await log_to_knowledge_vault(f"{protocol_name.lower().replace(' ', '_')}_conflict", {"idea": idea, "message": check_result.message})
            raise Exception(f"Nexus conflict detected: {check_result.message}")
        elif check_result.status == "waiting_on_dependency":
            await log_to_knowledge_vault(f"{protocol_name.lower().replace(' ', '_')}_waiting", {"idea": idea, "message": check_result.message})
            # In a real scenario, this might involve retries or a different handling
            # For now, we'll just proceed after the simulated delay
            pass
        return await func(*args, **kwargs)

    # 1. Code Generation
    try:
        generated_code = await _run_with_nexus_check("Code Generation", "start", generate_code, CodeGenerationInput(idea=idea))
        await log_to_knowledge_vault("code_generation_completed", {"idea": idea, "status": generated_code.status, "message": generated_code.message}, log_level="INFO", source_agent="CodeGenerator")
        
        if generated_code.status == "failure":
            await log_to_knowledge_vault("code_generation_failed_early_exit", {"idea": idea, "message": "Code generation failed, exiting orchestration."}, log_level="ERROR", source_agent="Orchestrator")
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
        security_report = await _run_with_nexus_check("Security Scan", "start", run_security_scan, generated_code.code)
        await log_to_knowledge_vault("security_scan_completed", {"idea": idea, "status": security_report.status, "findings_count": len(security_report.findings)}, log_level="INFO", source_agent="SecurityAgent")
        
        if security_report.status == "failed":
            await log_to_knowledge_vault("security_scan_failed_early_exit", {"idea": idea, "message": "Security scan failed, exiting orchestration."}, log_level="ERROR", source_agent="Orchestrator")
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
        # Assuming a summary of the generated code is enough for basic IaC generation
        infrastructure_input = InfrastructureInput(application_code_summary=generated_code.code[:200]) # Pass a summary
        infrastructure_results = await _run_with_nexus_check("Infrastructure Generation", "start", generate_infrastructure_code, infrastructure_input)
        await log_to_knowledge_vault("infrastructure_generation_completed", {"idea": idea, "status": infrastructure_results.status, "iac_code_summary": infrastructure_results.iac_code[:100]}, log_level="INFO", source_agent="InfrastructureAgent")
        
        if infrastructure_results.status == "failed":
            await log_to_knowledge_vault("infrastructure_generation_failed_early_exit", {"idea": idea, "message": "Infrastructure generation failed, exiting orchestration."}, log_level="ERROR", source_agent="Orchestrator")
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
        testing_input = TestingInput(code=generated_code.code, file_structure=generated_code.file_structure, dependencies=generated_code.dependencies)
        testing_results = await _run_with_nexus_check("Automated Testing", "start", run_tests, testing_input)
        await log_to_knowledge_vault("testing_completed", {"idea": idea, "overall_status": testing_results.status, "test_results_summary": [r.status for r in testing_results.test_results]}, log_level="INFO", source_agent="TestingAgent")
        
        if testing_results.status == "failure":
            await log_to_knowledge_vault("testing_failed_early_exit", {"idea": idea, "message": "Automated testing failed, exiting orchestration."}, log_level="ERROR", source_agent="Orchestrator")
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
        deployment_input = DeploymentInput(code=generated_code.code, test_status=testing_results.status, file_structure=generated_code.file_structure, dependencies=generated_code.dependencies, infrastructure_results=infrastructure_results)
        deployment_results = await _run_with_nexus_check("Automated Deployment", "start", deploy_application, deployment_input)
        await log_to_knowledge_vault("deployment_completed", {"idea": idea, "status": deployment_results.status, "url": deployment_results.deployment_url}, log_level="INFO", source_agent="DeploymentAgent")
        
        if deployment_results.status == "failure":
            await log_to_knowledge_vault("deployment_failed_early_exit", {"idea": idea, "message": "Automated deployment failed, exiting orchestration."}, log_level="ERROR", source_agent="Orchestrator")
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
        # For demonstration, let's assume we integrate a dummy analytics service
        integration_input = IntegrationInput(service_name="Dummy Analytics", api_endpoint="https://api.dummy-analytics.com", file_structure=generated_code.file_structure, dependencies=generated_code.dependencies, deployment_results=deployment_results)
        integration_results = await _run_with_nexus_check("External Service Integration", "start", integrate_external_service, integration_input)
        await log_to_knowledge_vault("integration_completed", {"idea": idea, "service": integration_input.service_name, "status": integration_results.status}, log_level="INFO", source_agent="IntegrationAgent")
        
        # No early return for integration failure, as it's the last step, but we log it.
        
        return GenesisResponse(
            idea=idea,
            generated_code=generated_code,
            security_report=security_report,
            infrastructure_results=infrastructure_results,
            testing_results=testing_results,
            deployment_results=deployment_results,
            integration_results=integration_results
        )
    except Exception as e:
        await log_to_knowledge_vault("orchestration_error", {"idea": idea, "error": str(e)}, log_level="CRITICAL", source_agent="Orchestrator")
        # Re-raise the exception or handle it as appropriate for the API
        raise e
