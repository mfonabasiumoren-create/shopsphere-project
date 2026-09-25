from flask import Flask, jsonify

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)