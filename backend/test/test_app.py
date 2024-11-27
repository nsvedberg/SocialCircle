import pytest
from app import create_app

@pytest.fixture
def client():
    """Fixture for setting up Flask test client."""
    app = create_app()
    app.config['TESTING'] = True  # Enables testing mode in Flask
    with app.test_client() as client:
        yield client  # Flask test client to make requests

def test_home_route(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data  # Check response content
