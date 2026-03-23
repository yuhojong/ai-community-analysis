"""Tests for the main application endpoints."""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_main():
    """Test the root endpoint returns a success message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Community Insights Analyzer API is running"}
