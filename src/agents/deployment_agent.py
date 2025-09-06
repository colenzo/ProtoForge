import random
import random
import os
import tempfile
import shutil
import subprocess
import docker
from pydantic import BaseModel
from typing import List, Dict, Optional

from src.agents.infrastructure_agent import InfrastructureOutput

class DeploymentInput(BaseModel):
    code: str
    test_status: str
    file_structure: Dict[str, List[str]]
    dependencies: List[str]
    infrastructure_results: Optional[InfrastructureOutput] = None
    # Potentially add more parameters like target_environment, cloud_provider, etc.

class DeploymentOutput(BaseModel):
    status: str  # e.g., "success", "failure", "pending", "warnings"
    message: str
    deployment_url: str = None
    # Potentially add more details like logs, resource_ids, etc.

async def deploy_application(input: DeploymentInput) -> DeploymentOutput:
    """Performs automated deployment of the generated application using Docker."""
    print(f"[DEPLOYMENT_AGENT] Attempting deployment for code... with test status: {input.test_status}")
    print(f"[DEPLOYMENT_AGENT] File structure: {input.file_structure}, Dependencies: {input.dependencies}")
    if input.infrastructure_results: print(f"[DEPLOYMENT_AGENT] Infrastructure status: {input.infrastructure_results.status}")
    
    deployment_status = "failure"
    deployment_message = "Deployment failed."
    deployment_url = None

    if input.test_status == "failure":
        deployment_message = "Deployment skipped due to failed tests."
        return DeploymentOutput(
            status=deployment_status,
            message=deployment_message,
            deployment_url=deployment_url
        )

    if input.infrastructure_results and input.infrastructure_results.status == "failed":
        deployment_message = "Deployment skipped due to failed infrastructure generation."
        return DeploymentOutput(
            status=deployment_status,
            message=deployment_message,
            deployment_url=deployment_url
        )

    # Create a temporary directory to build the Docker image
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"[DEPLOYMENT_AGENT] Working in temporary directory: {tmpdir}")

        # Write generated code to files in the temporary directory
        # This is a simplified version; in a real scenario, file_writer would be used
        # and code_content would be parsed for multiple files.
        main_app_file_path = None
        if input.file_structure and input.code:
            first_dir = list(input.file_structure.keys())[0]
            if input.file_structure[first_dir]:
                first_file = input.file_structure[first_dir][0]
                target_dir = os.path.join(tmpdir, first_dir)
                os.makedirs(target_dir, exist_ok=True)
                main_app_file_path = os.path.join(target_dir, first_file)
                with open(main_app_file_path, "w") as f:
                    f.write(input.code)
                print(f"[DEPLOYMENT_AGENT] Wrote main app file to: {main_app_file_path}")

        # Create a simple Dockerfile based on dependencies
        dockerfile_content = ""
        if "flask" in input.dependencies:
            dockerfile_content = f"""
FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/app.py .
EXPOSE 5000
CMD ["python", "app.py"] 
"""
            # Create a dummy requirements.txt for Flask app
            with open(os.path.join(tmpdir, "requirements.txt"), "w") as f:
                f.write("flask\n")
elif "pandas" in input.dependencies:
            dockerfile_content = f"""
FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY scripts/analyze.py .
CMD ["python", "analyze.py"]
"""
            with open(os.path.join(tmpdir, "requirements.txt"), "w") as f:
                f.write("pandas\nnumpy\n")
else:
            dockerfile_content = f"""
FROM python:3.9-slim-buster
WORKDIR /app
COPY src/main.py .
EXPOSE 8000
CMD ["python", "main.py"]
"""
            with open(os.path.join(tmpdir, "requirements.txt"), "w") as f:
                f.write("fastapi\nuvicorn\n")

        with open(os.path.join(tmpdir, "Dockerfile"), "w") as f:
            f.write(dockerfile_content)
        print(f"[DEPLOYMENT_AGENT] Wrote Dockerfile to: {os.path.join(tmpdir, 'Dockerfile')}")

        # Build Docker image
        try:
            client = docker.from_env()
            image_name = f"project-genesis-app:{random.randint(1000, 9999)}"
            print(f"[DEPLOYMENT_AGENT] Building Docker image: {image_name}")
            image, build_logs = client.images.build(path=tmpdir, tag=image_name, rm=True)
            for chunk in build_logs:
                if 'stream' in chunk:
                    print(f"[DOCKER_BUILD] {chunk['stream'].strip()}")
            print(f"[DEPLOYMENT_AGENT] Docker image built: {image.id}")

            # Run Docker container
            print(f"[DEPLOYMENT_AGENT] Running Docker container from image: {image_name}")
            container = client.containers.run(image_name, detach=True, ports={'5000/tcp': None, '8000/tcp': None})
            container.reload()
            
            # Get exposed port
            port_bindings = container.ports
            exposed_port = None
            if '5000/tcp' in port_bindings and port_bindings['5000/tcp']:
                exposed_port = port_bindings['5000/tcp'][0]['HostPort']
            elif '8000/tcp' in port_bindings and port_bindings['8000/tcp']:
                exposed_port = port_bindings['8000/tcp'][0]['HostPort']

            if exposed_port:
                deployment_status = "success"
                deployment_message = "Application deployed successfully to Docker."
                deployment_url = f"http://localhost:{exposed_port}"
                print(f"[DEPLOYMENT_AGENT] Application accessible at: {deployment_url}")
            else:
                deployment_status = "warnings"
                deployment_message = "Application deployed, but no port exposed or detected."
                print("[DEPLOYMENT_AGENT] No port exposed or detected.")

            # Clean up container after a short while (for simulation)
            # await asyncio.sleep(5) # In a real scenario, this would be managed externally
            # container.stop()
            # container.remove()

        except docker.errors.BuildError as e:
            deployment_message = f"Docker image build failed: {e}"
            print(f"[DEPLOYMENT_AGENT] Docker build error: {e}")
        except docker.errors.APIError as e:
            deployment_message = f"Docker API error during deployment: {e}"
            print(f"[DEPLOYMENT_AGENT] Docker API error: {e}")
        except Exception as e:
            deployment_message = f"An unexpected error occurred during Docker deployment: {e}"
            print(f"[DEPLOYMENT_AGENT] Unexpected error: {e}")

    return DeploymentOutput(
        status=deployment_status,
        message=deployment_message,
        deployment_url=deployment_url
    )
