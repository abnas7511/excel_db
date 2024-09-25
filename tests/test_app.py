import pytest
from io import BytesIO
from src.app import app, session
from src.db_config import UserInfo
import pandas as pd

@pytest.fixture
def client():
    """Setup the Flask test client."""
    app.config['TESTING'] = True  # Enable testing mode
    client = app.test_client()    # Create the test client
    yield client

    # Cleanup database after each test
    session.query(UserInfo).delete()
    session.commit()

def test_index(client):
    """Test the index route '/'."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"html" in response.data  # Assuming you return an HTML page

def test_upload_file(client):
    """Test the bulk file upload route '/upload'."""
    # Create a mock Excel file
    data = {
        'User': ['John Doe'],
        'Email ID': ['john@example.com'],
        'Role': ['Admin'],
        'Application Mapped': ['App1'],
        'License Type': ['Premium']
    }
    df = pd.DataFrame(data)
    with BytesIO() as b_io:
        df.to_excel(b_io, index=False)
        b_io.seek(0)
        data = {
            'file': (b_io, 'test.xlsx')
        }

        response = client.post('/upload', content_type='multipart/form-data', data=data)
        assert response.status_code == 200
        assert b"Data uploaded and stored successfully" in response.data

def test_upload_file_invalid_format(client):
    """Test uploading a non-Excel file to '/upload'."""
    data = {
        'file': (BytesIO(b"Invalid content"), 'test.txt')
    }
    response = client.post('/upload', content_type='multipart/form-data', data=data)
    assert response.status_code == 400
    assert b"Invalid file format" in response.data

def test_insert_user(client):
    """Test adding a user with POST request to '/users'."""
    data = {
        'user': 'Jane Doe',
        'emailid': 'jane@example.com',
        'role': 'Manager',
        'application_mapped': 'App2',
        'license_type': 'Standard'
    }
    response = client.post('/users', json=data)
    assert response.status_code == 201
    assert b"User added successfully" in response.data

def test_get_users(client):
    """Test retrieving all users with GET request to '/users'."""
    # Insert a test user into the database
    user = UserInfo(user='Jane Doe', emailid='jane@example.com', role='Manager',
                    application_mapped='App2', license_type='Standard')
    session.add(user)
    session.commit()

    response = client.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['user'] == 'Jane Doe'

def test_update_user(client):
    """Test updating a user with PUT request to '/users/<id>'."""
    # Insert a test user into the database
    user = UserInfo(user='Jane Doe', emailid='jane@example.com', role='Manager',
                    application_mapped='App2', license_type='Standard')
    session.add(user)
    session.commit()

    data = {
        'user': 'Jane Updated',
        'emailid': 'janeupdated@example.com'
    }
    response = client.put(f'/users/{user.id}', json=data)
    assert response.status_code == 200
    assert b"User with ID" in response.data

def test_delete_user(client):
    """Test deleting a user with DELETE request to '/users/<id>'."""
    # Insert a test user into the database
    user = UserInfo(user='John Doe', emailid='john@example.com', role='Admin',
                    application_mapped='App1', license_type='Premium')
    session.add(user)
    session.commit()

    response = client.delete(f'/users/{user.id}')
    assert response.status_code == 200
    assert b"User with ID" in response.data
