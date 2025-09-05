import requests
import json

BASE_URL = "http://localhost:8000/genesis"

def run_genesis_process(idea: str):
    print(f"\n--- Initiating Project Genesis for idea: '{idea}' ---")
    payload = {"idea": idea}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(f"{BASE_URL}/idea", data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        genesis_response = response.json()
        
        print("\n--- Project Genesis Results ---")
        print(f"Idea: {genesis_response.get('idea')}")
        
        generated_code = genesis_response.get('generated_code', {})
        print(f"\nCode Generation Status: {generated_code.get('status')}")
        print(f"  Message: {generated_code.get('message')}")
        if generated_code.get('code'):
            print(f"  Generated Code Snippet:\n---\n{generated_code.get('code')[:200]}...\n---")
        if generated_code.get('file_structure'):
            print(f"  File Structure: {generated_code.get('file_structure')}")
        if generated_code.get('dependencies'):
            print(f"  Dependencies: {generated_code.get('dependencies')}")

        security_report = genesis_response.get('security_report', {})
        if security_report:
            print(f"\nSecurity Scan Status: {security_report.get('status')}")
            print(f"  Message: {security_report.get('overall_message')}")
            for finding in security_report.get('findings', []):
                print(f"    - [{finding.get('severity')}] {finding.get('description')} (Location: {finding.get('location')})")

        infrastructure_results = genesis_response.get('infrastructure_results', {})
        if infrastructure_results:
            print(f"\nInfrastructure Generation Status: {infrastructure_results.get('status')}")
            print(f"  Message: {infrastructure_results.get('message')}")
            if infrastructure_results.get('iac_code'):
                print(f"  IaC Code Snippet:\n---\n{infrastructure_results.get('iac_code')[:200]}...\n---")

        testing_results = genesis_response.get('testing_results', {})
        if testing_results:
            print(f"\nAutomated Testing Status: {testing_results.get('status')}")
            print(f"  Message: {testing_results.get('overall_message')}")
            for test in testing_results.get('test_results', []):
                print(f"    - [{test.get('status')}] {test.get('test_name')}: {test.get('message')}")

        deployment_results = genesis_response.get('deployment_results', {})
        if deployment_results:
            print(f"\nAutomated Deployment Status: {deployment_results.get('status')}")
            print(f"  Message: {deployment_results.get('message')}")
            if deployment_results.get('deployment_url'):
                print(f"  Deployment URL: {deployment_results.get('deployment_url')}")

        integration_results = genesis_response.get('integration_results', {})
        if integration_results:
            print(f"\nExternal Service Integration Status: {integration_results.get('status')}")
            print(f"  Message: {integration_results.get('message')}")
            if integration_results.get('integration_id'):
                print(f"  Integration ID: {integration_results.get('integration_id')}")

    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the Project Genesis API. Is the FastAPI server running? (Run: python src/main.py)")
    except requests.exceptions.RequestException as e:
        print(f"\nERROR: An API request error occurred: {e}")
    except json.JSONDecodeError:
        print("\nERROR: Failed to decode JSON response from the API. Invalid response.")

if __name__ == "__main__":
    print("\nProject Genesis CLI - Enter your idea to start the process.")
    print("Type 'exit' to quit.")
    while True:
        user_idea = input("\nEnter your idea: ")
        if user_idea.lower() == 'exit':
            break
        run_genesis_process(user_idea)
