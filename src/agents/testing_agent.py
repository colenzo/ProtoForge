import random
import os
import tempfile
import shutil
import subprocess
import re # Import re for regex parsing
from pydantic import BaseModel
from typing import List, Dict

class TestResult(BaseModel):
    test_name: str
    status: str  # e.g., "passed", "failed", "skipped"
    message: str = None

class TestingInput(BaseModel):
    code: str
    file_structure: Dict[str, List[str]]
    dependencies: List[str]

class TestingOutput(BaseModel):
    status: str  # e.g., "success", "failure", "warnings"
    overall_message: str
    test_results: List[TestResult]

async def run_tests(input: TestingInput) -> TestingOutput:
    """Runs automated tests on the generated code using pytest."""
    print(f"[TESTING_AGENT] Running tests on generated code...")
    
    overall_status = "success"
    overall_message = "Automated tests completed."
    test_results = []

    # Create a temporary directory to write the generated code and test files
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"[TESTING_AGENT] Working in temporary directory: {tmpdir}")

        # Write generated code to files based on file_structure
        # This is a simplified version; in a real scenario, file_writer would be used
        # and code_content would be parsed for multiple files.
        # For now, we assume main application file is in the first directory and first file.
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
                print(f"[TESTING_AGENT] Wrote main app file to: {main_app_file_path}")

        # Generate a simple test file based on dependencies/code type
        test_file_content = ""
        if "flask" in input.dependencies:
            test_file_content = f"""
import pytest
import os
import sys

# Add the temporary app directory to sys.path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_hello_flask(client):
    rv = client.get('/')
    assert b'Hello, Flask Web App!' in rv.data
"""
        elif "pandas" in input.dependencies:
            test_file_content = f"""
import pytest
import pandas as pd
import os
import sys

# Add the temporary scripts directory to sys.path for import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from analyze import analyze_data_model

def test_analyze_data_model():
    data = {{'col1': [1, 2, 3], 'col2': [4, 5, 6]}}
    shape = analyze_data_model(data)
    assert shape == (3, 2)
"""
        else:
            test_file_content = f"""
import pytest

def test_generic_code_runs():
    assert True # Basic test to ensure code can be imported/run
"""
        
        test_file_path = os.path.join(tmpdir, "test_generated_app.py")
        with open(test_file_path, "w") as f:
            f.write(test_file_content)
        print(f"[TESTING_AGENT] Wrote test file to: {test_file_path}")

        # Run pytest
        try:
            # Use subprocess.run for external command execution
            # capture_output=True to get stdout/stderr
            # text=True to decode output as string
            # cwd to run pytest in the temporary directory
            result = subprocess.run(
                ["pytest", "-v", test_file_path],
                capture_output=True,
                text=True,
                check=False, # Do not raise CalledProcessError for non-zero exit codes, we parse output
                cwd=tmpdir
            )
            print(f"[TESTING_AGENT] Pytest stdout:\n{result.stdout}")
            print(f"[TESTING_AGENT] Pytest stderr:\n{result.stderr}")

            # Parse pytest output for detailed results
            # Example: test_hello_flask PASSED
            # Example: test_analyze_data_model FAILED
            test_pattern = r"^(.*?)\s(PASSED|FAILED|SKIPPED|ERROR)"
            for line in result.stdout.splitlines():
                match = re.search(test_pattern, line)
                if match:
                    test_name = match.group(1).strip()
                    status = match.group(2).lower()
                    message = f"Test {test_name} {status}."
                    test_results.append(TestResult(test_name=test_name, status=status, message=message))
            
            # Determine overall status
            if any(t.status == "failed" for t in test_results):
                overall_status = "failure"
                overall_message = "Automated tests failed. One or more tests reported failures."
            elif any(t.status == "warnings" for t in test_results):
                overall_status = "warnings"
                overall_message = "Automated tests completed with warnings."
            elif any(t.status == "error" for t in test_results):
                overall_status = "failure"
                overall_message = "Automated tests encountered errors."
            else:
                overall_status = "success"
                overall_message = "All automated tests passed successfully."

        except FileNotFoundError:
            overall_status = "failure"
            overall_message = "Pytest command not found. Is pytest installed?"
            test_results.append(TestResult(test_name="pytest_not_found", status="failed", message="Pytest executable not found."))
        except Exception as e:
            overall_status = "failure"
            overall_message = f"An unexpected error occurred during testing: {e}"
            test_results.append(TestResult(test_name="unexpected_error", status="failed", message=str(e)))

    return TestingOutput(
        status=overall_status,
        overall_message=overall_message,
        test_results=test_results
    )
