import unittest

from app.app import app


class ShopSphereAPITests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {"status": "healthy"}
        )

    def test_home_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "application": "ShopSphere",
                "message": "Welcome to ShopSphere E-Commerce API",
                "status": "running"
            }
        )

    def test_create_order_requires_order_data(self):
        response = self.client.post("/orders", json={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Order data is required"}
        )

    def test_create_order_requires_product_and_quantity(self):
        response = self.client.post(
            "/orders",
            json={"product_id": 1}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "product_id and quantity are required"}
        )

    def test_create_order_rejects_non_positive_quantity(self):
        response = self.client.post(
            "/orders",
            json={"product_id": 1, "quantity": 0}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Quantity must be a positive integer"}
        )

if __name__ == "__main__":
    unittest.main()