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


if __name__ == "__main__":
    unittest.main()