import random
from faker import Faker
import mysql.connector


product_names = [
    "Dell XPS 13", "Dell XPS 15", "Dell Inspiron 14", "Dell Latitude 7420", 
    "Dell Precision 5550", "Dell G15 Gaming", "Dell Alienware m15", 
    "Dell OptiPlex 3090", "Dell Vostro 3500", "Dell Chromebook 3100",
    "Dell UltraSharp Monitor", "Dell Dock WD19", "Dell PowerEdge T40", 
    "Dell EMC Unity XT", "Dell Wyse 5070", "Dell G7 17 Gaming", 
    "Dell Inspiron 7000", "Dell P2422H Monitor", "Dell Rugged Extreme 7220", 
    "Dell Alienware Aurora R12", "Dell OptiPlex 7080", "Dell Latitude 5420", 
    "Dell Inspiron 15 3000", "Dell G3 Gaming", "Dell UltraSharp Webcam"
]


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="dell_computers"
)
cursor = conn.cursor()


faker = Faker()


def populate_products():
    for product in product_names:
        product_price = round(random.uniform(100, 2000), 2)
        product_stock = random.randint(10, 100)
        product_description = faker.sentence(nb_words=10)
        product_category = random.choice(["Laptop", "Monitor", "Desktop", "Accessory"])
        is_dell = 1

        cursor.execute(
            """INSERT INTO products (product_name, product_price, product_description, product_stock, product_category, is_dell)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (product, product_price, product_description, product_stock, product_category, is_dell)
        )
    conn.commit()


def populate_customers(n):
    for _ in range(n):
        customer_fname = faker.first_name()
        customer_lname = faker.last_name()
        address = faker.address()
        phone_number = faker.phone_number()

        cursor.execute(
            """INSERT INTO customers (customer_fname, customer_lname, address, phone_number)
            VALUES (%s, %s, %s, %s)""",
            (customer_fname, customer_lname, address, phone_number)
        )
    conn.commit()


def populate_sales(n):
    product_ids = [i for i in range(1, len(product_names) + 1)]
    customer_ids = [i for i in range(1, n + 1)]

    for _ in range(n):
        sale_total_value = round(random.uniform(100, 5000), 2)
        quantity_sold = random.randint(1, 10)
        customer_id = random.choice(customer_ids)
        status = random.choice(["Completed", "Pending", "Cancelled"])

        # Insert into sales table
        cursor.execute(
            """INSERT INTO sales (sale_total_value, quantity_sold, customers_id, status)
            VALUES (%s, %s, %s, %s)""",
            (sale_total_value, quantity_sold, customer_id, status)
        )
        sale_id = cursor.lastrowid

        # Insert into product_sales table
        for _ in range(random.randint(1, 3)):
            product_id = random.choice(product_ids)
            cursor.execute(
                """INSERT INTO product_sales (sales_id, products_id)
                VALUES (%s, %s)""",
                (sale_id, product_id)
            )
    conn.commit()

# Populate the tables
populate_products()
populate_customers(25)  # Insert 25 customers
populate_sales(25)      # Insert 25 sales


cursor.close()
conn.close()
