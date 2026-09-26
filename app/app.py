from flask import Flask, jsonify, request

app = Flask(__name__)


products = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "category": "Electronics",
        "price": 45000,
        "stock": 25
    },
    {
        "id": 2,
        "name": "Running Shoes",
        "category": "Fashion",
        "price": 32000,
        "stock": 18
    },
    {
        "id": 3,
        "name": "Smart Watch",
        "category": "Electronics",
        "price": 75000,
        "stock": 12
    }
]

orders = []


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
    return jsonify({
        "count": len(products),
        "products": products
    })


@app.route("/products/<int:product_id>")
def get_product(product_id):
    product = next(
        (product for product in products if product["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product)
@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify({
        "count": len(orders),
        "orders": orders
    })

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

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