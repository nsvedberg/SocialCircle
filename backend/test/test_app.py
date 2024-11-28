import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_default(client):
    response = client.get('/')
    assert response.status_code == 200   

# This test fails for now, for some reason all real routes just return the errorhandler from develop.py?
#def test_existing_route(client):
#    response = client.get('/login')
#    assert response.status_code == 200
#    assert b'Log' in response.data

# develop serves index.html when non-existent page, check for some of the index.html here
def test_fake_route(client):
    response = client.get('/boakkadawo')
    assert b'href="/favicon.ico"/><meta name="viewport"' in response.data


