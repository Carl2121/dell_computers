from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "dell_computers"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

#CUSTOMERS
@app.route("/customers", methods=["GET"])
def get_customers():
    data = data_fetch("""SELECT * FROM customers""")
    return make_response(jsonify(data), 200)

@app.route("/customers/<int:id>", methods=["GET"])
def get_customer_by_id(id):
    data = data_fetch("""SELECT * FROM customers where id = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/customers", methods=["POST"])
def add_customer():
    cur = mysql.connection.cursor()
    info = request.get_json()
    customer_fname = info["customer_fname"]
    customer_lname = info["customer_lname"]
    address = info["address"]
    phone_number = info["phone_number"]
    cur.execute(
        """ INSERT INTO customers (customer_fname, customer_lname, address, phone_number) VALUE (%s, %s, %s, %s)""",
        (customer_fname, customer_lname, address, phone_number),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "customer added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@app.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    customer_fname = info["customer_fname"]
    customer_lname = info["customer_lname"]
    address = info["address"]
    phone_number = info["phone_number"]
    cur.execute(
        """ UPDATE customers SET customer_fname = %s, customer_lname = %s, address = %s, phone_number = %s WHERE id = %s """,
        (customer_fname, customer_lname, address, phone_number, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "customer updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM customers where id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "customer deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

#PRODUCTS
@app.route("/products", methods=["GET"])
def get_products():
    data = data_fetch("""SELECT * FROM products""")
    return make_response(jsonify(data), 200)


@app.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    data = data_fetch("""SELECT * FROM products where id = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/products", methods=["POST"])
def add_product():
    cur = mysql.connection.cursor()
    info = request.get_json()
    product_name = info["product_name"]
    product_price = info["product_price"]
    product_description = info["product_description"]
    product_stock = info["product_stock"]
    product_category = info["product_category"]
    is_dell = info["is_dell"]
    cur.execute(
        """ INSERT INTO products (product_name, product_price, product_description, product_stock, product_category, is_dell) VALUE (%s, %s, %s, %s, %s, %s)""",
        (product_name, product_price, product_description, product_stock, product_category, is_dell),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "product added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    product_name = info["product_name"]
    product_price = info["product_price"]
    product_description = info["product_description"]
    product_stock = info["product_stock"]
    product_category = info["product_category"]
    is_dell = info["is_dell"]

    cur.execute(
        """ UPDATE products SET product_name = %s, product_price = %s, product_description = %s, product_stock = %s, product_category = %s, is_dell = %s WHERE id = %s """,
        (product_name, product_price, product_description, product_stock, product_category, is_dell, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "product updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM products where id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "product deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )


#SALES
@app.route("/sales", methods=["GET"])
def get_sales():
    data = data_fetch("""SELECT * FROM sales""")
    return make_response(jsonify(data), 200)


@app.route("/sales/<int:id>", methods=["GET"])
def get_sale_by_id(id):
    data = data_fetch("""SELECT * FROM sales where id = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/sales", methods=["POST"])
def add_sale():
    cur = mysql.connection.cursor()
    info = request.get_json()
    sale_total_value = info["sale_total_value"]
    quantity_sold = info["quantity_sold"]
    customers_id = info["customers_id"]
    status = info["status"]

    cur.execute(
        """ INSERT INTO sales (sale_total_value, quantity_sold, customers_id, status) VALUE (%s, %s, %s, %s)""",
        (sale_total_value, quantity_sold, customers_id, status),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "sale added successfully", "rows_affected": rows_affected}
        ),
        201,
    )

@app.route("/sales/<int:id>", methods=["PUT"])
def update_sale(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    sale_total_value = info["sale_total_value"]
    quantity_sold = info["quantity_sold"]
    customers_id = info["customers_id"]
    status = info["status"]

    cur.execute(
        """ UPDATE sales SET sale_total_value = %s , quantity_sold = %s, customers_id = %s, status = %s WHERE id = %s """,
        (sale_total_value, quantity_sold, customers_id, status, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "sale updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/sales/<int:id>", methods=["DELETE"])
def delete_sale(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM sales where id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "sale deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

#PRODUCT SALES
@app.route("/product_sales", methods=["GET"])
def get_product_sales():
    data = data_fetch("""SELECT * FROM product_sales""")
    return make_response(jsonify(data), 200)


@app.route("/product_sales/<int:sales_id>/<int:products_id>", methods=["GET"])
def get_product_sale_by_id(sales_id, products_id):
    data = data_fetch(
        """SELECT * FROM product_sales WHERE sales_id = {} AND products_id = {}""".format(
            sales_id, products_id
        )
    )
    return make_response(jsonify(data), 200)

@app.route("/product_sales", methods=["POST"])
def add_product_sale():
    cur = mysql.connection.cursor()
    info = request.get_json()
    sales_id = info["sales_id"]
    products_id = info["products_id"]

    cur.execute(
        """ INSERT INTO product_sales (sales_id, products_id) VALUES (%s, %s)""",
        (sales_id, products_id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {
                "message": "product_sale added successfully",
                "rows_affected": rows_affected,
            }
        ),
        201,
    )

@app.route("/product_sales/<int:sales_id>/<int:products_id>", methods=["PUT"])
def update_product_sale(sales_id, products_id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    new_sales_id = info["sales_id"]
    new_products_id = info["products_id"]

    cur.execute(
        """ UPDATE product_sales SET sales_id = %s, products_id = %s WHERE sales_id = %s AND products_id = %s """,
        (new_sales_id, new_products_id, sales_id, products_id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {
                "message": "product_sale updated successfully",
                "rows_affected": rows_affected,
            }
        ),
        200,
    )

@app.route("/product_sales/<int:sales_id>/<int:products_id>", methods=["DELETE"])
def delete_product_sale(sales_id, products_id):
    cur = mysql.connection.cursor()
    cur.execute(
        """ DELETE FROM product_sales WHERE sales_id = %s AND products_id = %s """,
        (sales_id, products_id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {
                "message": "product_sale deleted successfully",
                "rows_affected": rows_affected,
            }
        ),
        200,
    )

if __name__ == "__main__":
    app.run(debug=True)