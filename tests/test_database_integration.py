import unittest

from app.app import app, get_db_connection


class ShopSphereDatabaseIntegrationTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_endpoint_reads_from_mysql(self):
        response = self.client.get("/products")

        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["count"], 3)
        self.assertEqual(len(data["products"]), 3)

        product_names = {
            product["name"]
            for product in data["products"]
        }

        self.assertEqual(
            product_names,
            {
                "Wireless Headphones",
                "Running Shoes",
                "Smart Watch",
            },
        )

    def test_create_order_updates_mysql(self):
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO products (name, category, price, stock)
                    VALUES (%s, %s, %s, %s)
                    """,
                    ("Integration Test Product", "Testing", 100.00, 5),
                )
                product_id = cursor.lastrowid

            connection.commit()
        finally:
            connection.close()

        try:
            response = self.client.post(
                "/orders",
                json={"product_id": product_id, "quantity": 2},
            )

            self.assertEqual(response.status_code, 201)

            data = response.get_json()
            self.assertEqual(data["order"]["product_id"], product_id)
            self.assertEqual(data["order"]["quantity"], 2)
            self.assertEqual(data["order"]["total"], "200.00")

            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT stock FROM products WHERE id = %s",
                        (product_id,),
                    )
                    product = cursor.fetchone()

                    cursor.execute(
                        """
                        SELECT product_id, quantity, total
                        FROM orders
                        WHERE product_id = %s
                        """,
                        (product_id,),
                    )
                    order = cursor.fetchone()

                self.assertEqual(product["stock"], 3)
                self.assertEqual(order["product_id"], product_id)
                self.assertEqual(order["quantity"], 2)
                self.assertEqual(float(order["total"]), 200.00)
            finally:
                connection.close()

        finally:
            connection = get_db_connection()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM orders WHERE product_id = %s",
                        (product_id,),
                    )
                    cursor.execute(
                        "DELETE FROM products WHERE id = %s",
                        (product_id,),
                    )
                connection.commit()
            finally:
                connection.close()


if __name__ == "__main__":
    unittest.main()