from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "dell_computers"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["SECRET_KEY"] = "ss_marschiert"

mysql = MySQL(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request"}), 400)

# JWT Authentication Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorizations")
        if not token:
            return make_response(jsonify({"error": "You need a token to access this endpoint!"}), 401)
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user = data
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({"error": "Token has expired"}), 401)
        except jwt.InvalidTokenError:
            return make_response(jsonify({"error": "Invalid token"}), 401)
        return f(*args, **kwargs)
    return decorated

# Role-based Access Control Decorator
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(request, "user") or request.user.get("role") != role:
                return make_response(jsonify({"error": "Access forbidden"}), 403)
            return f(*args, **kwargs)
        return decorated
    return decorator

# Generate JWT Token
@app.route("/login", methods=["POST"])
def login():
    auth = request.get_json()
    if not auth or not auth.get("username") or not auth.get("password"):
        return make_response(jsonify({"error": "Username and password required"}), 400)

    username = auth["username"]
    password = auth["password"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cur.fetchone()
    cur.close()

    if not user:
        return make_response(jsonify({"error": "Invalid credentials"}), 401)

    token = jwt.encode(
        {
            "user_id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    return jsonify({"token": token})

@app.route("/")
def index_page():
    return "<h1><strong>Welcome To Dell Computers and Electronics!</strong></h1>"

def data_fetch(query, params=None):
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, params or ())
        data = cur.fetchall()
        cur.close()
        return data
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# Input validation helpers (for the CRUD hehe)

def validate_customer_input(data):
    required_fields = ["customer_fname", "customer_lname", "address", "phone_number"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return f"Missing fields: {', '.join(missing_fields)}"
    return None

def validate_product_input(data):
    required_fields = ["product_name", "product_price", "product_description", "product_stock", "product_category", "is_dell"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return f"Missing fields: {', '.join(missing_fields)}"
    return None

def validate_sales_input(data):
    required_fields = ["sale_total_value", "quantity_sold", "customers_id", "status"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return f"Missing fields: {', '.join(missing_fields)}"
    return None

def validate_product_sales_input(data):
    required_fields = ["products_id", "sales_id"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return f"Missing fields: {', '.join(missing_fields)}"
    return None


# CUSTOMERS CRUD
@app.route("/customers", methods=["GET"])
@token_required
def get_customers():
    try:
        data = data_fetch("SELECT * FROM customers")
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/customers/<int:id>", methods=["GET"])
@token_required
def get_customer_by_id(id):
    try:
        data = data_fetch("SELECT * FROM customers WHERE id = %s", (id,))
        if not data:
            return make_response(jsonify({"error": "Customer not found"}), 404)
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/customers", methods=["POST"])
def add_customer():
    try:
        info = request.get_json()
        validation_error = validate_customer_input(info)
        if validation_error:
            return make_response(jsonify({"error": validation_error}), 400)

        cur = mysql.connection.cursor()
        cur.execute(
            """ INSERT INTO customers (customer_fname, customer_lname, address, phone_number) 
            VALUES (%s, %s, %s, %s) """,
            (
                info["customer_fname"],
                info["customer_lname"],
                info["address"],
                info["phone_number"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "customer added successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    try:
        info = request.get_json()
        validation_error = validate_customer_input(info)
        if validation_error:
            return make_response(jsonify({"error": validation_error}), 400)

        cur = mysql.connection.cursor()
        cur.execute(
            """ UPDATE customers SET customer_fname = %s, customer_lname = %s, address = %s, phone_number = %s 
            WHERE id = %s """,
            (
                info["customer_fname"],
                info["customer_lname"],
                info["address"],
                info["phone_number"],
                id,
            ),
        )
        mysql.connection.commit()
        if cur.rowcount == 0:
            return make_response(jsonify({"error": "Customer not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "customer updated successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM customers WHERE id = %s", (id,))
        mysql.connection.commit()
        if cur.rowcount == 0:
            return make_response(jsonify({"error": "Customer not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "customer deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# PRODUCTS CRUD
@app.route("/products", methods=["GET"])
def get_products():
    try:
        data = data_fetch("SELECT * FROM products")
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    try:
        data = data_fetch("SELECT * FROM products WHERE id = %s", (id,))
        if not data:
            return make_response(jsonify({"error": "Product not found"}), 404)
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/products", methods=["POST"])
def add_product():
    try:
        info = request.get_json()
        validation_error = validate_product_input(info)
        if validation_error:
            return make_response(jsonify({"error": validation_error}), 400)

        cur = mysql.connection.cursor()
        cur.execute(
            """ INSERT INTO products (product_name, product_price, product_description, product_stock, product_category, is_dell) 
            VALUES (%s, %s, %s, %s, %s, %s) """,
            (
                info["product_name"],
                info["product_price"],
                info["product_description"],
                info["product_stock"],
                info["product_category"],
                info["is_dell"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "product added successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    try:
        info = request.get_json()
        validation_error = validate_product_input(info)
        if validation_error:
            return make_response(jsonify({"error": validation_error}), 400)

        cur = mysql.connection.cursor()
        cur.execute(
            """ UPDATE products SET product_name = %s, product_price = %s, product_description = %s, product_stock = %s, product_category = %s, is_dell = %s 
            WHERE id = %s """,
            (
                info["product_name"],
                info["product_price"],
                info["product_description"],
                info["product_stock"],
                info["product_category"],
                info["is_dell"],
                id,
            ),
        )
        mysql.connection.commit()
        if cur.rowcount == 0:
            return make_response(jsonify({"error": "Product not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "product updated successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM products WHERE id = %s", (id,))
        mysql.connection.commit()
        if cur.rowcount == 0:
            return make_response(jsonify({"error": "Product not found"}), 404)
        cur.close()
        return make_response(jsonify({"message": "product deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# SALES CRUD
@app.route("/sales", methods=["GET"])
def get_sales():
    try:
        data = data_fetch("SELECT * FROM sales")
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/sales/<int:id>", methods=["GET"])
def get_sale_by_id(id):
    try:
        data = data_fetch("SELECT * FROM sales WHERE id = %s", (id,))
        if not data:
            return make_response(jsonify({"error": "sale not found"}), 404)
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/sales", methods=["POST"])
def add_sale():
    try:
        info = request.get_json()
        validation_error = validate_sales_input(info)
        if validation_error:
            return make_response(jsonify({"error": validation_error}), 400)

        cur = mysql.connection.cursor()
        cur.execute(
            """ INSERT INTO sales (sale_total_value, quantity_sold, customers_id, status) 
            VALUES (%s, %s, %s, %s) """,
            (
                info["sale_total_value"],
                info["quantity_sold"],
                info["customers_id"],
                info["status"],
            ),
        )
        mysql.connection.commit()
        cur.close()
        return make_response(jsonify({"message": "sale added successfully"}), 201)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)



@app.route("/sales/<int:id>", methods=["PUT"])
def update_sale(id):
    try:
        info = request.get_json()
        validation_error = validate_sales_input(info)
        if validation_error:
            return make_response(jsonify({"error": validation_error}), 400)

        cur = mysql.connection.cursor()
        cur.execute(
            """ UPDATE sales SET sale_total_value = %s, quantity_sold = %s, customers_id = %s, status = %s 
            WHERE id = %s """,
            (info["sale_total_value"], info["quantity_sold"], info["customers_id"], info["status"], id),
        )
        mysql.connection.commit()
        rows_affected = cur.rowcount
        if rows_affected == 0:
            return make_response(jsonify({"error": "Sale not found"}), 404)
        cur.close()
        return make_response(
            jsonify({"message": "sale updated successfully", "rows_affected": rows_affected}), 200
        )
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/sales/<int:id>", methods=["DELETE"])
def delete_sale(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM sales WHERE id = %s", (id,))
        mysql.connection.commit()
        rows_affected = cur.rowcount
        cur.close()
        if rows_affected == 0:
            return make_response(jsonify({"error": "Sale not found"}), 404)
        return make_response(
            jsonify({"message": "sale deleted successfully", "rows_affected": rows_affected}), 200
        )
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# PRODUCTS SALES CRUD
@app.route("/product_sales", methods=["GET"])
def get_product_sales():
    try:
        data = data_fetch("SELECT * FROM product_sales")
        if not data:
            return make_response(jsonify({"error": "No product sales found"}), 404)
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)


@app.route("/product_sales/<int:sales_id>/<int:products_id>", methods=["GET"])
def get_product_sale_by_id(sales_id, products_id):
    try:
        data = data_fetch(
            "SELECT * FROM product_sales WHERE sales_id = %s AND products_id = %s",
            (sales_id, products_id),
        )
        if not data:
            return make_response(
                jsonify({"error": "Product sale not found for the given IDs"}), 404
            )
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/product_sales", methods=["POST"])
def add_product_sale():
    try:
        info = request.get_json()
        validation_error = validate_product_sales_input(info)
        if validation_error:
            return make_response(jsonify({"error": validation_error}), 400)

        cur = mysql.connection.cursor()
        cur.execute(
            """ INSERT INTO product_sales (sales_id, products_id) VALUES (%s, %s)""",
            (info["sales_id"], info["products_id"]),
        )
        mysql.connection.commit()
        rows_affected = cur.rowcount
        cur.close()
        return make_response(
            jsonify({"message": "product sale added successfully", "rows_affected": rows_affected}), 201
        )
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

@app.route("/product_sales/<int:sales_id>/<int:products_id>", methods=["PUT"])
def update_product_sale(sales_id, products_id):
    try:
        info = request.get_json()
        validation_error = validate_product_sales_input(info)
        if validation_error:
            return make_response(jsonify({"error": validation_error}), 400)

        cur = mysql.connection.cursor()
        cur.execute(
            """ UPDATE product_sales SET sales_id = %s, products_id = %s 
            WHERE sales_id = %s AND products_id = %s """,
            (info["sales_id"], info["products_id"], sales_id, products_id),
        )
        mysql.connection.commit()
        rows_affected = cur.rowcount
        if rows_affected == 0:
            return make_response(jsonify({"error": "Product sale not found"}), 404)
        cur.close()
        return make_response(
            jsonify({"message": "product sale updated successfully", "rows_affected": rows_affected}), 200
        )
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
    
@app.route("/product_sales/<int:sales_id>/<int:products_id>", methods=["DELETE"])
def delete_product_sale(sales_id, products_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """ DELETE FROM product_sales WHERE sales_id = %s AND products_id = %s """,
            (sales_id, products_id),
        )
        mysql.connection.commit()
        rows_affected = cur.rowcount
        cur.close()
        if rows_affected == 0:
            return make_response(jsonify({"error": "Product sale not found"}), 404)
        return make_response(
            jsonify({"message": "product sale deleted successfully", "rows_affected": rows_affected}), 200
        )
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# STORY 1
@app.route("/sales/<int:sale_id>/status", methods=["GET"])
def get_purchase_status(sale_id):
    try:
        query = """
            SELECT 
                sales.id AS sale_id, 
                sales.status, 
                sales.sale_total_value, 
                sales.quantity_sold, 
                sales.customers_id
            FROM sales
            WHERE sales.id = %s
        """
        data = data_fetch(query, (sale_id,))
        
        if not data:
            return make_response(jsonify({"error": "No purchase found for this sale ID"}), 404)
        
        return make_response(jsonify(data[0]), 200)  # Return the first matching record
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)



# STORY 2
@app.route("/products/<int:product_id>/stock", methods=["GET"])
def get_product_stock(product_id):
    try:
        data = data_fetch("SELECT product_stock FROM products WHERE id = %s", (product_id,))
        if not data:
            return make_response(jsonify({"error": "Product not found"}), 404)
        return make_response(jsonify({"product_id": product_id, "stock": data[0]["product_stock"]}), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

# STORY 3
@app.route("/customers/<int:customer_id>/purchases", methods=["GET"])
def get_purchases_by_customer(customer_id):
    try:
        # Fetch purchases made by the customer
        query = """
            SELECT 
                sales.id AS sale_id, 
                sales.sale_total_value, 
                sales.quantity_sold, 
                sales.status, 
                products.product_name, 
                products.product_price 
            FROM sales
            JOIN product_sales ON sales.id = product_sales.sales_id
            JOIN products ON product_sales.products_id = products.id
            WHERE sales.customers_id = %s
        """
        data = data_fetch(query, (customer_id,))
        
        if not data:
            return make_response(jsonify({"error": "No purchases found for this customer"}), 404)
        
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)

if __name__ == "__main__":
    app.run(debug=True)