import pytest
from unittest.mock import patch, AsyncMock
from src.agents.code_generator import generate_code, CodeGenerationInput, GeneratedCode
from src.core.lumen_analyzer import get_latest_lumen_insights # Import for mocking
import random # Import random for mocking

@pytest.mark.asyncio
async def test_generate_code_success_flask():
    with patch('src.agents.code_generator._call_ai_code_model', new_callable=AsyncMock) as mock_call_ai_code_model:
        mock_call_ai_code_model.return_value = {
            "status": "success",
            "message": "Model generated Flask app.",
            "generated_text": "--- FILE: app/app.py ---\nfrom flask import Flask\napp = Flask(__name__)\n\n@app.route('/')\ndef hello_flask():\n    return 'Hello, Flask Web App!'\n",
            "type": "flask"
        }
        with patch('src.agents.code_generator.get_latest_lumen_insights', return_value={}) as mock_lumen_insights:
            # Mock random.choices to always return 'ok'
            with patch('random.choices', return_value=['ok']):
                input_idea = CodeGenerationInput(idea="create a simple web app with flask")
                result = await generate_code(input_idea)

                assert result.status == "success"
                assert "Flask" in result.message
                assert "app/app.py" in result.code
                assert result.file_structure == {"app": ["app.py"], "templates": ["index.html"]}
                assert "flask" in result.dependencies

@pytest.mark.asyncio
async def test_generate_code_ai_error():
    with patch('src.agents.code_generator._call_ai_code_model', new_callable=AsyncMock) as mock_call_ai_code_model:
        mock_call_ai_code_model.return_value = {
            "status": "error",
            "message": "AI model encountered an internal error.",
            "generated_text": ""
        }
        with patch('src.agents.code_generator.get_latest_lumen_insights', return_value={}) as mock_lumen_insights:
            # Mock random.choices to ensure deterministic behavior even for error case
            with patch('random.choices', return_value=['ok']):
                input_idea = CodeGenerationInput(idea="generate code with error")
                result = await generate_code(input_idea)

                assert result.status == "failure"
                assert "AI model encountered an internal error." in result.message
                assert "# ERROR: AI model failed to generate code." in result.code
                assert result.file_structure == {}
                assert result.dependencies == []

