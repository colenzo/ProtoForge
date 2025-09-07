from fastapi.testclient import TestClient
from src.main import app # Assuming genesis router is included in main app

client = TestClient(app)

def test_test_route():
    response = client.get("/genesis/test") # Note the prefix /genesis
    assert response.status_code == 200
    assert response.json() == {"message": "test route works"}