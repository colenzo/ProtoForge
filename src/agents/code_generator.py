import random
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict, Any
from src.core.lumen_analyzer import get_latest_lumen_insights

# Load environment variables from .env file
load_dotenv()

class CodeGenerationInput(BaseModel):
    idea: str
    # Potentially add more parameters like target_language, framework, etc.

class GeneratedCode(BaseModel):
    status: str
    message: str
    code: str
    file_structure: Dict[str, List[str]] = {}
    dependencies: List[str] = []

async def _call_ai_code_model(prompt: str) -> Dict[str, Any]:
    """Simulates an API call to a real AI code generation model."""
    # In a real scenario, this would use requests or an SDK to call OpenAI, Gemini, etc.
    # For now, we'll just simulate loading an API key and returning a response.
    
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        print("WARNING: AI API key not found in environment variables. Using fallback simulation.")
        return {"status": "error", "message": "API key missing.", "generated_text": ""}

    print(f"Simulating AI model call with prompt: {prompt[:100]}...")
    
    # Simulate different model responses based on prompt keywords
    if "web app" in prompt.lower() or "flask" in prompt.lower():
        generated_text = f"""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_flask():
    return 'Hello, Flask Web App! Idea: {prompt}'
"""
        return {"status": "success", "message": "Model generated Flask app.", "generated_text": generated_text, "type": "flask"}
    elif "data analysis" in prompt.lower() or "pandas" in prompt.lower():
        generated_text = f"""
import pandas as pd

def analyze_data_model(data):
    df = pd.DataFrame(data)
    return df.describe().to_dict()
"""
        return {"status": "success", "message": "Model generated Pandas script.", "generated_text": generated_text, "type": "pandas"}
    elif "error" in prompt.lower() or random.random() < 0.1: # Simulate occasional model errors
        return {"status": "error", "message": "AI model encountered an internal error.", "generated_text": ""}
    else:
        generated_text = f"""
# Generic AI-generated code for: {prompt}
print("Hello from AI!")
"""
        return {"status": "success", "message": "Model generated generic code.", "generated_text": generated_text, "type": "generic"}

async def generate_code(input: CodeGenerationInput) -> GeneratedCode:
    """Simulates AI-driven code generation logic based on the idea."""
    print(f"Generating code for idea: {input.idea}")
    
    ai_model_response = await _call_ai_code_model(input.idea)

    code_content = ai_model_response.get("generated_text", "")
    file_structure = {}
    dependencies = []
    status = "success"
    message = ai_model_response.get("message", "Code generation initiated.")

    if ai_model_response.get("status") == "error":
        status = "failure"
        message = ai_model_response.get("message", "AI model failed to generate code.")
        code_content = "# ERROR: AI model failed to generate code.\n"
        return GeneratedCode(
            status=status,
            message=message,
            code=code_content,
            file_structure=file_structure,
            dependencies=dependencies
        )

    # Determine file structure and dependencies based on simulated AI model output type
    if ai_model_response.get("type") == "flask":
        file_structure = {"app": ["app.py"], "templates": ["index.html"]}
        dependencies = ["flask"]
    elif ai_model_response.get("type") == "pandas":
        file_structure = {"scripts": ["analyze.py"], "data": ["sample.csv"]}
        dependencies = ["pandas", "numpy"]
    else:
        file_structure = {"src": ["main.py"]}
        dependencies = ["fastapi", "uvicorn"]

    # Simulate different outcomes (minor issues) after initial generation
    # Adjust weights based on Lumen insights
    lumen_insights = get_latest_lumen_insights()
    current_weights = [0.8, 0.2] # ok, minor_issues
    if lumen_insights and "Enhance code generation model's robustness for complex ideas." in lumen_insights.get("suggested_improvements", []):
        print("[CODE_GENERATOR] Adjusting generation based on Lumen insights: improving robustness.")
        current_weights = [0.9, 0.1] # Increase success chance

    outcome_post_ai = random.choices(['ok', 'minor_issues'], weights=current_weights, k=1)[0]

    if outcome_post_ai == 'minor_issues':
        status = "warnings"
        message += " Code generated with minor warnings. Review suggested for optimization or style issues."
        code_content += "\n# WARNING: Potential style issue detected.\n"
        if "flask" in dependencies: dependencies.append("gunicorn")
        elif "pandas" in dependencies: dependencies.append("matplotlib")

    return GeneratedCode(
        status=status,
        message=message,
        code=code_content,
        file_structure=file_structure,
        dependencies=dependencies
    )
