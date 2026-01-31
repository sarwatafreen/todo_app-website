from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
    print("✓ Health endpoint test passed!")

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    print("✓ Root endpoint test passed!")

if __name__ == "__main__":
    print("Running API tests...")
    test_health_endpoint()
    test_root_endpoint()
    print("✓ All API tests passed!")