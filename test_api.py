import pytest
from api import app

@pytest.fixture
def mock_db(mocker):
    """Mock the MySQL database connection and cursor."""
    mock_conn = mocker.patch('flask_mysqldb.MySQL.connection')
    mock_cursor = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_cursor

@pytest.fixture
def client():
    """Fixture to provide a Flask test client."""
    with app.test_client() as client:
        with app.app_context():
            yield client

# Test: GET /customers
def test_get_customers(client, mock_db):
    mock_db.fetchall.return_value = [
        {
            "address": "197 Emily Curve Suite 810\nMoniquefurt, TN 96599",
            "customer_fname": "Robert",
            "customer_lname": "Gonzalez",
            "id": 1,
            "phone_number": "788.896.7541x64859"
        }
    ]  
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json[0] ['customer_fname'] == "Robert"



# Test: GET /customers/<id>
def test_get_customer_by_id(client, mock_db):
    mock_db.fetchall.return_value = [{ "customer_fname": "Samantha"}]  
    response = client.get("/customers/2")
    assert response.status_code == 200
    assert response.json[0] ['customer_fname'] == "Samantha"

# # Test: POST /customers
def test_add_customer(client, mock_db):
    mock_db.rowcount = 1  # Mock successful insertion
    response = client.post(
        '/customers',
        json={
            "customer_fname": "Stalin",
            "customer_lname": "Comrade",
            "address": "123 Dell Street",
            "phone_number": "1234567890",
        },
    )
    assert response.status_code == 201
    assert b"customer added successfully" in response.data
    assert response.json["rows_affected"] == 1


# # Test: PUT /customers/<id>
def test_update_customer(client, mock_db):
    mock_db.rowcount = 1
    response = client.put('/customers/1', 
        json={
            "address": "197 Emily Curve Suite 810\nMoniquefurt, TN 96599",
            "customer_fname": "Robert",
            "customer_lname": "Gonzalez",
            "id": 1,
            "phone_number": "788.896.7541x64859"})
    assert response.status_code == 200
    assert b"customer updated successfully" in response.data
    assert response.json["rows_affected"] == 1


# Test: DELETE /customers/<id>
def test_delete_customer(client, mock_db):
    mock_db.rowcount = 1
    response = client.delete('/customers/1')
    assert response.status_code == 200
    assert b"customer deleted successfully" in response.data
    assert response.json["rows_affected"] == 1


