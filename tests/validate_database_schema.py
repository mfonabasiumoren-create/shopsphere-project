import os
import sys
from pathlib import Path

import pymysql
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env.integration"), override=True)

EXPECTED_COLUMNS = {
    "products": {
        "id": "int",
        "name": "varchar",
        "category": "varchar",
        "price": "decimal",
        "stock": "int",
        "created_at": "timestamp",
    },
    "orders": {
        "id": "int",
        "product_id": "int",
        "quantity": "int",
        "total": "decimal",
        "created_at": "timestamp",
    },
}


def validate_schema():
    if os.getenv("DB_NAME") != "shopsphere_test":
        raise RuntimeError(
            "Schema validation must use the shopsphere_test database."
        )

    connection = pymysql.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = {
                next(iter(row.values()))
                for row in cursor.fetchall()
            }

            for table, expected_columns in EXPECTED_COLUMNS.items():
                if table not in tables:
                    raise AssertionError(
                        f"Required table is missing: {table}"
                    )

                cursor.execute(f"SHOW COLUMNS FROM `{table}`")
                actual_columns = {
                    row["Field"]: row["Type"].split("(")[0].lower()
                    for row in cursor.fetchall()
                }

                for column, expected_type in expected_columns.items():
                    actual_type = actual_columns.get(column)

                    if actual_type != expected_type:
                        raise AssertionError(
                            f"{table}.{column}: expected "
                            f"{expected_type}, got {actual_type}"
                        )

                cursor.execute(f"SHOW KEYS FROM `{table}`")
                primary_keys = {
                    row["Column_name"]
                    for row in cursor.fetchall()
                    if row["Key_name"] == "PRIMARY"
                }

                if "id" not in primary_keys:
                    raise AssertionError(
                        f"{table} must have id as its primary key."
                    )

            cursor.execute(
                """
                SELECT COUNT(*) AS foreign_key_count
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s
                  AND TABLE_NAME = 'orders'
                  AND COLUMN_NAME = 'product_id'
                  AND REFERENCED_TABLE_NAME = 'products'
                  AND REFERENCED_COLUMN_NAME = 'id'
                """,
                (os.environ["DB_NAME"],),
            )

            result = cursor.fetchone()

            if result["foreign_key_count"] != 1:
                raise AssertionError(
                    "orders.product_id must reference products.id."
                )

        print("Database schema validation passed.")
    finally:
        connection.close()


if __name__ == "__main__":
    try:
        validate_schema()
    except Exception as error:
        print(
            f"Database schema validation failed: {error}",
            file=sys.stderr,
        )
        sys.exit(1)