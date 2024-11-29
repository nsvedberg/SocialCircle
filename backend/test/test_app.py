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
        'club_email': 'Test email',
        'club_creator': {
            'id': 1  
        }
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

# Test comments
def test_create_edit_delete_comments(client):
    # Create a club to put comments on, using same code from club tests
    club_response = client.post('/b/clubs/new', json={
        'club_name': 'Test Club',
        'club_description': 'A test description',
        'club_email': 'Test email',
        'club_creator': {
            'id': 1
        }
    })

    assert club_response.status_code == 201
    created_club = club_response.get_json()
    club_id = created_club['id']

    # Test comment creation
    comment_creation_response = client.post(f'/b/clubs/{club_id}/comments', json={
        'comment': 'Test comment',
        'creator_id': 3  # Assumes there is a user in db with id3, current its carol lee
    })

    assert comment_creation_response.status_code == 201
    created_comment = comment_creation_response.get_json()
    assert created_comment['comment'] == 'Test comment'
    assert created_comment['creator_id'] == 3
    assert created_comment['user']['first_name'] == 'Carol'  
    assert created_comment['user']['last_name'] == 'Lee'

    # get all comments for the club, check if the comment exists, and there is only one comment
    comments_response = client.get(f'/b/clubs/{club_id}/comments')
    assert comments_response.status_code == 200
    comments = comments_response.get_json()
    assert len(comments) == 1
    assert comments[0]['comment'] == 'Test comment'
    assert comments[0]['creator_id'] == 3

    # Tst comment edit
    comment_id = created_comment['comment_id']
    comment_edit_response = client.post(f'/b/clubs/{club_id}/comments/{comment_id}/edit', json={
        'comment': 'Updated test comment'
    })
    assert comment_edit_response.status_code == 200
    updated_comment = comment_edit_response.get_json()
    assert updated_comment['comment'] == 'Updated test comment'

    # Test comment delete
    comment_delete_response = client.delete(f'/b/clubs/{club_id}/comments/{comment_id}/delete')
    assert comment_delete_response.status_code == 200

    # Verify the comment deleteion was a success by checking if there are any more comments
    comments_response_after_delete = client.get(f'/b/clubs/{club_id}/comments')
    comments_after_delete = comments_response_after_delete.get_json()
    assert len(comments_after_delete) == 0

    # Delete the club that we created for this test
    delete_response = client.delete(f'/b/clubs/{club_id}')
    assert delete_response.status_code == 200
    deleted_club = delete_response.get_json()
    assert deleted_club['id'] == club_id 
    assert deleted_club['club_name'] == 'Test Club' # Check that the deleted club was the club

    # Check that the club no longer exists on the clubs list page
    view_response = client.get('/b/clubs')
    assert b'Updated Test Club' not in view_response.data 
# TODO: User tests

#Search Tests
def test_search_by_name(client):
    # Create a club for testing
    creation_response = client.post('/b/clubs/new', json={
        'club_name': 'Test Club Search By Name',
        'club_description': 'A description for name search',
        'club_email': 'test@email.com',
        'club_creator': {
            'id': 1  
        }
    })
    created_club = creation_response.get_json()
    club_id = created_club['id']  # Save the club ID for later use

    # Search by name
    search_term = 'Test Club Search By Name'
    search_response = client.get(f'/b/clubs/name/{search_term}')
    
    print("Search Response Data:", search_response.data)  # Print response for debugging
    assert search_response.status_code == 200
    search_results = search_response.get_json()

    # Inspect the structure of search_results to debug the issue
    print("Search Results JSON:", search_results)

    assert len(search_results) > 0
    assert search_results[0]['club_name'] == 'Test Club Search By Name'
    
    delete_response = client.delete(f'/b/clubs/{club_id}')
    assert delete_response.status_code == 200


def test_search_by_id(client):
    # Create a club for testing
    creation_response = client.post('/b/clubs/new', json={
        'club_name': 'Test Club Search By ID',
        'club_description': 'A description for ID search',
        'club_email': 'test@email.com',
        'club_creator': {
            'id': 1  
        }
    })
    created_club = creation_response.get_json()
    club_id = created_club['id']  # Save the club ID for later use

    # Search by ID
    search_response = client.get(f'/b/clubs/id/{club_id}')
    
    print("Search Response Data:", search_response.data)  # Print response for debugging
    assert search_response.status_code == 200
    search_results = search_response.get_json()

    # Inspect the structure of search_results to debug the issue
    print("Search Results JSON:", search_results)

    assert len(search_results) == 1  # Ensure exactly 1 result is returned
    assert search_results[0]['club_name'] == 'Test Club Search By ID'
    assert search_results[0]['club_description'] == 'A description for ID search'
    
    delete_response = client.delete(f'/b/clubs/{club_id}')
    assert delete_response.status_code == 200


def test_search_by_description(client):
    # Create a club for testing
    creation_response = client.post('/b/clubs/new', json={
        'club_name': 'Test Club Search By Description',
        'club_description': 'A description for description search',
        'club_email': 'test@email.com',
        'club_creator': {
            'id': 1  
        }
    })
    created_club = creation_response.get_json()
    club_id = created_club['id']  # Save the club ID for later use

    # Search by description
    search_term = 'description search'
    search_response = client.get(f'/b/clubs/description/{search_term}')
    
    print("Search Response Data:", search_response.data)  # Print response for debugging
    assert search_response.status_code == 200
    search_results = search_response.get_json()

    # Inspect the structure of search_results to debug the issue
    print("Search Results JSON:", search_results)

    assert len(search_results) > 0  # Ensure some results are returned
    assert any(club['club_name'] == 'Test Club Search By Description' for club in search_results)
    assert any(club['club_description'] == 'A description for description search' for club in search_results)
    
    delete_response = client.delete(f'/b/clubs/{club_id}')
    assert delete_response.status_code == 200

def test_search_no_results(client):
    # Perform a search with a term that does not exist in the database
    search_term = 'Non-existent club'
    search_response = client.get(f'/b/clubs/name/{search_term}')
    assert search_response.status_code == 404
    error_response = search_response.get_json()
    assert error_response['error'] == 'No clubs found'

def test_search_invalid_attribute(client):
    # Try searching with an invalid attribute (e.g., an attribute other than name, id, or description)
    search_term = 'Some term'
    search_response = client.get(f'/b/clubs/invalid/{search_term}')
    assert search_response.status_code == 400
    error_response = search_response.get_json()
    assert error_response['error'] == 'Invalid search attribute'

# TODO: Other feature tests (messaging, rsvp, reccomendations)?





