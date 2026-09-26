from flask import Flask, jsonify, request
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "shopsphere")
DB_USER = os.getenv("DB_USER", "shopsphere_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

def get_db_connection():
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection



@app.route("/")
def home():
    return jsonify({
        "application": "ShopSphere",
        "message": "Welcome to ShopSphere E-Commerce API",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/products")
def get_products():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            products_from_db = cursor.fetchall()

        return jsonify({
            "count": len(products_from_db),
            "products": products_from_db
        })
    finally:
        connection.close()

@app.route("/products/<int:product_id>")
def get_product(product_id):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM products WHERE id = %s",
                (product_id,)
            )
            product = cursor.fetchone()

        if product is None:
            return jsonify({"error": "Product not found"}), 404

        return jsonify(product)
    finally:
        connection.close()
@app.route("/orders", methods=["GET"])
def get_orders():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    orders.id AS order_id,
                    orders.product_id,
                    products.name AS product_name,
                    orders.quantity,
                    orders.total,
                    orders.created_at
                FROM orders
                JOIN products ON orders.product_id = products.id
                ORDER BY orders.id
            """)
            orders_from_db = cursor.fetchall()

        return jsonify({
            "count": len(orders_from_db),
            "orders": orders_from_db
        })
    finally:
        connection.close()

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Order data is required"}), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if product_id is None or quantity is None:
        return jsonify({"error": "product_id and quantity are required"}), 400

    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM products WHERE id = %s FOR UPDATE",
                (product_id,)
            )
            product = cursor.fetchone()

            if product is None:
                return jsonify({"error": "Product not found"}), 404

            if quantity > product["stock"]:
                return jsonify({"error": "Insufficient stock"}), 400

            total = product["price"] * quantity

            cursor.execute(
                """
                INSERT INTO orders (product_id, quantity, total)
                VALUES (%s, %s, %s)
                """,
                (product_id, quantity, total)
            )

            order_id = cursor.lastrowid

            cursor.execute(
                """
                UPDATE products
                SET stock = stock - %s
                WHERE id = %s
                """,
                (quantity, product_id)
            )

        connection.commit()

        return jsonify({
            "message": "Order created successfully",
            "order": {
                "order_id": order_id,
                "product_id": product_id,
                "product_name": product["name"],
                "quantity": quantity,
                "total": str(total)
            }
        }), 201

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close() 
    if not data:
        return jsonify({
            "error": "Order data is required"
        }), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if product_id is None or quantity is None:
        return jsonify({
            "error": "product_id and quantity are required"
        }), 400

    product = next(
        (product for product in products if product["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({
            "error": "Quantity must be a positive integer"
        }), 400

    if quantity > product["stock"]:
        return jsonify({
            "error": "Insufficient stock"
        }), 400

    total = product["price"] * quantity

    order = {
        "order_id": len(orders) + 1,
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "total": total
    }

    orders.append(order)

    product["stock"] -= quantity

    return jsonify({
        "message": "Order created successfully",
        "order": order
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)