import pytest
from api import app
from unittest.mock import patch

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


# Test: POST /login
def test_login_success(client, mock_db):
    mock_db.fetchone.return_value = {
        "id": 1,
        "username": "testuser",
        "role": "admin"
    }
    response = client.post('/login', json={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "token" in response.json

def test_login_failure(client, mock_db):
    mock_db.fetchone.return_value = None
    response = client.post('/login', json={"username": "wronguser", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json["error"] == "Invalid credentials"

# Test: Error Handlers
def test_404_error_handler(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
    assert response.json["error"] == "Not found"

def test_400_error_handler(client):
    response = client.post('/customers', json={})
    assert response.status_code == 400
    assert response.json["error"] == "Missing fields: customer_fname, customer_lname, address, phone_number"

# Test: Role-based Access Control
@patch('api.token_required', lambda x: x)
@patch('api.role_required', lambda role: lambda x: x)
def test_role_based_access(client, mock_db):
    mock_db.fetchall.return_value = [
        {
            "address": "197 Emily Curve Suite 810\nMoniquefurt, TN 96599",
            "customer_fname": "Robert",
            "customer_lname": "Gonzalez",
            "id": 1,
            "phone_number": "788.896.7541x64859"
        }
    ]
    response = client.get("/customers", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 401



# Test: GET /customers
@patch('api.token_required', lambda x: x)
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
    response = client.get("/customers", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 401
    

# Test: GET /customers/<id>
@patch('api.token_required', lambda x: x)
def test_get_customer_by_id(client, mock_db):
    mock_db.fetchall.return_value = [{"customer_fname": "Samantha"}]
    response = client.get("/customers/2", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 401
    

# Test: POST /customers
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
    


# Test: DELETE /customers/<id>
def test_delete_customer(client, mock_db):
    mock_db.rowcount = 1
    response = client.delete('/customers/1')
    assert response.status_code == 200
    assert b"customer deleted successfully" in response.data
    


# Test: GET /products
def test_get_products(client, mock_db):
    mock_db.fetchall.return_value = [
        {
            "product_name": "Dell XPS 13",
        }
    ]  
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json[0]['product_name'] == "Dell XPS 13"

# Test: GET /products/<id>
def test_get_product_by_id(client, mock_db):
    mock_db.fetchall.return_value = [{ "product_name": "Dell XPS 13" }]  
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json[0]['product_name'] == "Dell XPS 13"

# Test: POST /products
def test_add_product(client, mock_db):
    mock_db.rowcount = 1  # Mock successful insertion
    response = client.post(
        '/products',
        json={
            "product_name": "Keyboard",
            "product_price": 50,
            "product_description": "Mechanical keyboard",
            "product_stock": 200,
            "product_category": "Accessories",
            "is_dell": False
        },
    )
    assert response.status_code == 201
    assert b"product added successfully" in response.data
    


# Test: PUT /products/<id>
def test_update_product(client, mock_db):
    mock_db.rowcount = 1
    response = client.put('/products/1', 
        json={
            "product_name": "Mouse",
            "product_price": 25,
            "product_description": "Wireless mouse",
            "product_stock": 150,
            "product_category": "Accessories",
            "is_dell": False})
    assert response.status_code == 200
    assert b"product updated successfully" in response.data
    

# Test: DELETE /products/<id>
def test_delete_product(client, mock_db):
    mock_db.rowcount = 1
    response = client.delete('/products/1')
    assert response.status_code == 200
    assert b"product deleted successfully" in response.data
    


# Test: GET /sales
def test_get_sales(client, mock_db):
    mock_db.fetchall.return_value = [
        {
            "id": 1,
            "sale_total_value": 3754,
            "quantity_sold": 2
        }
    ]  
    response = client.get("/sales")
    assert response.status_code == 200
    assert response.json[0]['sale_total_value'] == 3754

# Test: GET /sales/<id>
def test_get_sale_by_id(client, mock_db):
    mock_db.fetchall.return_value = [{ "sale_total_value": 3754 }]  
    response = client.get("/sales/2")
    assert response.status_code == 200
    assert response.json[0]['sale_total_value'] == 3754

# Test: POST /sales
def test_add_sale(client, mock_db):
    mock_db.rowcount = 1  # Mock successful insertion
    response = client.post(
        '/sales',
        json={
            "sale_total_value": 500,
            "quantity_sold": 1,
            "customers_id": 1,
            "status": "completed"
        },
    )
    assert response.status_code == 201
    assert b"sale added successfully" in response.data
    

# Test: PUT /sales/<id>
def test_update_sale(client, mock_db):
    mock_db.rowcount = 1
    response = client.put('/sales/1', 
        json={
            "sale_total_value": 700,
            "quantity_sold": 2,
            "customers_id": 1,
            "status": "pending"})
    assert response.status_code == 200
    assert b"sale updated successfully" in response.data
    

# Test: DELETE /sales/<id>
def test_delete_sale(client, mock_db):
    mock_db.rowcount = 1
    response = client.delete('/sales/1')
    assert response.status_code == 200
    assert b"sale deleted successfully" in response.data
    

# Test: GET /product_sales
def test_get_product_sales(client, mock_db):
    mock_db.fetchall.return_value = [
        {
            "sales_id": 1,
            "products_id": 1
        }
    ]  
    response = client.get("/product_sales")
    assert response.status_code == 200
    assert response.json[0]['sales_id'] == 1

# Test: GET /product_sales/<sales_id>/<products_id>
def test_get_product_sale_by_id(client, mock_db):
    mock_db.fetchall.return_value = [{ "sales_id": 1, "products_id": 2 }]  
    response = client.get("/product_sales/1/2")
    assert response.status_code == 200
    assert response.json[0]['products_id'] == 2


# Test: POST /product_sales
def test_add_product_sale(client, mock_db):
    mock_db.rowcount = 1  # Mock successful insertion
    response = client.post(
        '/product_sales',
        json={
            "sales_id": 1,
            "products_id": 2
        },
    )
    assert response.status_code == 201
    assert b"product sale added successfully" in response.data
    

# Test: PUT /product_sales/<sales_id>/<products_id>
def test_update_product_sale(client, mock_db):
    mock_db.rowcount = 1
    response = client.put('/product_sales/1/2', 
        json={
            "sales_id": 1,
            "products_id": 2
        })
    assert response.status_code == 200
    assert b"product sale updated successfully" in response.data
    

# Test: DELETE /product_sales/<sales_id>/<products_id>
def test_delete_product_sale(client, mock_db):
    mock_db.rowcount = 1
    response = client.delete('/product_sales/1/2')
    assert response.status_code == 200
    assert b"product sale deleted successfully" in response.data
    
# Test: GET /sales/<sale_id>/status
def test_get_purchase_status(client, mock_db):
    mock_db.fetchall.return_value = [
        {
            "sale_id": 2,
            "status": "completed",
            "sale_total_value": 500,
            "quantity_sold": 1,
            "customers_id": 1
        }
    ]
    response = client.get("/sales/2/status")
    assert response.status_code == 200
    assert response.json['sale_id'] == 2
    assert response.json['status'] == "completed"
    assert response.json['sale_total_value'] == 500
    assert response.json['quantity_sold'] == 1

# Test: GET /products/<product_id>/stocks
def test_get_product_stock(client, mock_db):
    mock_db.fetchall.return_value = [
        {
            "product_name": "Dell XPS 13",
            "product_stock": 10
        }
    ]
    response = client.get("/products/4/stocks")
    assert response.status_code == 200
    assert response.json['product_id'] == 4
    assert response.json['product_name'] == "Dell XPS 13"
    assert response.json['stock'] == 10

# Test: GET /customers/<customer_id>/purchases
def test_get_purchases_by_customer(client, mock_db):
    mock_db.fetchall.return_value = [
        {
            "sale_id": 1,
            "sale_total_value": 3754,
            "quantity_sold": 2,
            "status": "completed",
            "product_name": "Dell XPS 13",
            "product_price": 1500
        }
    ]
    response = client.get("/customers/1/purchases")
    assert response.status_code == 200
    assert response.json[0]['sale_id'] == 1
    assert response.json[0]['sale_total_value'] == 3754
    assert response.json[0]['quantity_sold'] == 2
    assert response.json[0]['status'] == "completed"
    assert response.json[0]['product_name'] == "Dell XPS 13"
    assert response.json[0]['product_price'] == 1500







