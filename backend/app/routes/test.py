import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

# Test the create club method
def test_create_club(client):
    response = client.post('/clubs/new', data=dict(club_name='Test Name', club_description = "Test Description"), follow_redirects=True) # Create a new club, redirect to dashboard
    assert response.status_code == 200
    assert "Test Name" in response.data # Check if new club is on dashboard?
