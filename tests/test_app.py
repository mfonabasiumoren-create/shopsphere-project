import unittest

from unittest.mock import MagicMock, patch

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


    @patch("app.app.get_db_connection")
    def test_create_order_success(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.fetchone.return_value = {
            "id": 1,
            "name": "Wireless Headphones",
            "price": 32000,
            "stock": 10
        }
        mock_cursor.lastrowid = 101

        response = self.client.post(
            "/orders",
            json={"product_id": 1, "quantity": 2}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {
                "message": "Order created successfully",
                "order": {
                    "order_id": 101,
                    "product_id": 1,
                    "product_name": "Wireless Headphones",
                    "quantity": 2,
                    "total": "64000"
                }
            }
        )

        self.assertEqual(mock_cursor.execute.call_count, 3)
        mock_connection.commit.assert_called_once()
        mock_connection.rollback.assert_not_called()
        mock_connection.close.assert_called_once()
