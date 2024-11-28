import pytest
from app import app
from datetime import datetime

# Testing suite
# Run by using the command 'pytest', in the backend or socialcircle root directory.
# pytest must be installed from the requirements.txt
# Make sure each test that creates a new object (club, event, etc.) deletes it at the end, otherwise you will spam the db with test data like I did :)

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


# Event tests 
def test_create_view_edit_delete_event(client):
    event_date = datetime.now().isoformat() 
    creation_response = client.post('/b/events/new', json={
        'event_name': 'Test Event',
        'event_description': 'Test description',
        'event_location': 'Somewhere',
        'event_date': event_date,
        'event_time': '14:00',
        'event_club': 'Test club',
        'event_tags': 'Test tag'
    })
    assert creation_response.status_code == 201 # Successful creation
    created_event = creation_response.get_json()
    event_id = created_event['id'] # Get id for use in other tests

    view_response = client.get('/b/events')
    assert b'Test Event' in view_response.data # Check for newly created test event on dashboard

    # Edit event
    event_date_updated = datetime.utcnow()  # Use UTC for consistency with GMT
    # RFC 1123 format
    updated_rfc_1123_format = event_date_updated.strftime("%a, %d %b %Y %H:%M:%S GMT") # The date is in this format after creation, so have to convert it 
    edit_response = client.put(f'/b/events/{event_id}', json={
        'event_name': 'Updated Test Event3',
        'event_description': 'Updated Test description',
        'event_location': 'Somewhere v2',
        'event_date': updated_rfc_1123_format, 
        'event_time': '14:01',
        'event_club': 'Updated Test club',
        'event_tags': 'Updated Test tag'
    })
    assert edit_response.status_code == 200
    updated_event = edit_response.get_json()
    assert updated_event['event_name'] == 'Updated Test Event3'
    assert updated_event['event_description'] == 'Updated Test description'
    assert updated_event['event_location'] == 'Somewhere v2'
    assert updated_event['event_date'] == updated_rfc_1123_format
    assert updated_event['event_time'] == '14:01'

    # Delete event
    delete_response = client.delete(f'/b/events/{event_id}')
    assert delete_response.status_code == 200
    deleted_event = delete_response.get_json()
    assert deleted_event['id'] == event_id 
    assert deleted_event['event_name'] == 'Updated Test Event3' # Check that the deleted event was the event

    # Now check the event no longer exists on the events page
    view_response = client.get('/b/events')
    # NOTE: This assertion will not work if you go into the delete section with TWO events in event list with this test name.
    assert b'Updated Test Event3' not in view_response.data 

# TODO: Club comment tests (I will do these)
# TODO: User tests
# TODO: Search tests
# TODO: Other feature tests (messaging, rsvp, reccomendations)?





