import pytest
from api import app


@pytest.fixture
def client():
    """Fixture to set up the test client."""
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Mathnasium API"}

def test_get_attendance(client):
    """Test GET /attendance route."""
    response = client.get("/attendance")
    assert response.status_code == 200
    assert isinstance(response.json, dict) or isinstance(response.json, list)