import pytest
from app import app
from datetime import datetime

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

# Full testing suit for club functions, except for join club and comment
def test_create_view_edit_delete_club(client):
    creation_response = client.post('/b/clubs/new', json={
        'club_name': 'Test Club',
        'club_description': 'A test description',
        'club_email': 'Test email'
    })
    created_club = creation_response.get_json()
    club_id = created_club['id'] # Save this id, we will use the same club for the edited and delete tests
    assert created_club['club_name'] == 'Test Club'

    # After creating the club, that club title will be visible on the clubs page, check for that
    view_response = client.get('/b/clubs')
    assert b'Test Club' in view_response.data

    # TODO: Comment testing

    # Edit club
    edit_response = client.put(f'/b/clubs/{club_id}', json={
        'club_name': 'Updated Test Club',
        'club_description': 'Updated description',
        'club_email': 'updated@email.com'
    })
    assert edit_response.status_code == 200
    updated_club = edit_response.get_json()
    assert updated_club['club_name'] == 'Updated Test Club'
    assert updated_club['club_description'] == 'Updated description'
    assert updated_club['club_email'] == 'updated@email.com'

    # Delete club
    delete_response = client.delete(f'/b/clubs/{club_id}')
    assert delete_response.status_code == 200
    deleted_club = delete_response.get_json()
    assert deleted_club['id'] == club_id # Check that deleted club was the club we were trying to delete lol
    assert deleted_club['club_name'] == 'Updated Test Club' # Check that the deleted club was the club

    # Now check the club no longer exists on the clubs list page
    view_response = client.get('/b/clubs')
    assert b'Updated Test Club' not in view_response.data 


# Event tests (TODO: Add edit/delete like in the clubs testing above)
def test_create_event(client):
    event_date = datetime.now().isoformat() 
    response = client.post('/b/events/new', json={
        'event_name': 'Test Event',
        'event_description': 'Test description',
        'event_location': 'Somewhere',
        'event_date': event_date,
        'event_time': '14:00',
        'event_club': 'Test club',
        'event_tags': 'Test tag'
    })
    assert response.status_code == 201 # Successful creation
    response = client.get('/b/events')
    assert b'Test Event' in response.data # Check for newly created test event on dashboard

# TODO: Profile/Login tests
# TODO: Search bar tests





