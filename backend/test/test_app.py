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

# develop serves index.html when non-existent page, check for some of the index.html here
def test_fake_route(client):
    response = client.get('/boakkadawo')
    assert b'href="/favicon.ico"/><meta name="viewport"' in response.data

def test_create_club(client):
    response = client.post('/b/clubs/new', json={
        'club_name': 'Test Club',
        'club_description': 'A test description',
        'club_email': 'Test email'
    })
    response_data = response.get_json()
    assert response_data['name'] == 'Test Club'
    assert response_data['description'] == 'A test description'
    assert response_data['email'] == 'Test email'

    # After creating the club, that club title will be visible on the clubs page, check for that
    response = client.get('/b/clubs')
    assert b'Test Club' in response.data


