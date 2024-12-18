# Dell Computers and Electronics API

## Description

This project is a Flask-based API for managing customers, products, sales, and product sales for Dell Computers and Electronics. It includes JWT authentication and role-based access control.

## Installation

```cmd
pip install -r requirements.txt
```

## Configuration

To set up the database:

1. Create a MySQL database called dell_computers.
2. Update the database details in the Flask app.

Environment variables you need:

MYSQL_HOST: MySQL server (e.g., localhost). MYSQL_USER: Your MySQL username (e.g., root). MYSQL_PASSWORD: Your MySQL password. MYSQL_DB: Database name (e.g., dell_computers). SECRET_KEY: A secret key for the app (e.g., ss_marschiert).

Or set these directly in the code:
`app.config["MYSQL_HOST"] = "localhost"`
`app.config["MYSQL_USER"] = "root"`
`app.config["MYSQL_PASSWORD"] = "root"`
`app.config["MYSQL_DB"] = "dell_computers"`
`app.config["SECRET_KEY"] = "ss_marschiert"`

## Key notes

Only the customers entity require authentication.

## API Endpoints

| Endpoint                                | Method | Description                       |
| --------------------------------------- | ------ | --------------------------------- |
| /login                                  | POST   | Generate JWT token(For customers) |
| /customers                              | GET    | List all customers                |
| /customers                              | POST   | Create a new customer             |
| /customers/<id>                         | GET    | Get a customer by ID              |
| /customers/<id>                         | PUT    | Update a customer by ID           |
| /customers/<id>                         | DELETE | Delete a customer by ID           |
| /products                               | GET    | List all products                 |
| /products                               | POST   | Create a new product              |
| /products/<id>                          | GET    | Get a product by ID               |
| /products/<id>                          | PUT    | Update a product by ID            |
| /products/<id>                          | DELETE | Delete a product by ID            |
| /sales                                  | GET    | List all sales                    |
| /sales                                  | POST   | Create a new sale                 |
| /sales/<id>                             | GET    | Get a sale by ID                  |
| /sales/<id>                             | PUT    | Update a sale by ID               |
| /sales/<id>                             | DELETE | Delete a sale by ID               |
| /product_sales                          | GET    | List all product sales            |
| /product_sales                          | POST   | Create a new product sale         |
| /product_sales/<sales_id>/<products_id> | GET    | Get a product sale by IDs         |
| /product_sales/<sales_id>/<products_id> | PUT    | Update a product sale by IDs      |
| /product_sales/<sales_id>/<products_id> | DELETE | Delete a product sale by IDs      |
| /sales/<sale_id>/status                 | GET    | Get the status of a sale by ID    |
| /products/<product_id>/stocks           | GET    | Get the stock of a product by ID  |
| /customers/<customer_id>/purchases      | GET    | Get purchases by a customer ID    |

## Testing

Instructions for running tests:

```cmd
pytest test_api.py
```

## Git Commit Guidelines

Use conventional commits:

```bash
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
test: add user registration tests
```
