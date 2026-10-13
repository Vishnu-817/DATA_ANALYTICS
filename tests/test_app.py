import unittest
from datetime import date
from unittest.mock import patch

import app


class FakeCursor:
    def __init__(self, rows=None):
        self.rows = rows or []
        self.query = None
        self.params = None

    def execute(self, query, params=None):
        self.query = query
        self.params = params

    def fetchall(self):
        return self.rows

    def close(self):
        pass


class FakeConnection:
    def __init__(self, rows=None):
        self.menu_cursor = FakeCursor(rows)
        self.reservation_cursor = FakeCursor()
        self.committed = False

    def cursor(self, dictionary=False):
        return self.menu_cursor if dictionary else self.reservation_cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

    def is_connected(self):
        return True

    def close(self):
        pass


class RestaurantRoutesTest(unittest.TestCase):
    def setUp(self):
        app.app.config.update(TESTING=True)
        self.client = app.app.test_client()

    def valid_reservation(self):
        return {
            "name": "Alex Morgan",
            "email": "alex@example.com",
            "phone": "",
            "date": date.today().isoformat(),
            "time": "19:00",
            "guests": "2",
            "notes": "Window seat",
        }

    def test_home_and_static_assets(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        stylesheet = self.client.get("/styles.css")
        script = self.client.get("/app.js")
        self.assertEqual(stylesheet.status_code, 200)
        self.assertEqual(script.status_code, 200)
        stylesheet.close()
        script.close()

    @patch.object(app, "get_db_connection")
    def test_menu_returns_database_items(self, get_connection):
        get_connection.return_value = FakeConnection(
            [{"id": 1, "name": "Test Pasta", "price": 18}]
        )

        response = self.client.get("/api/menu")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["name"], "Test Pasta")

    def test_reservation_rejects_invalid_payload(self):
        response = self.client.post(
            "/api/reservations", json={"email": "not-an-email"}
        )

        self.assertEqual(response.status_code, 400)

    @patch.object(app, "get_db_connection")
    def test_reservation_is_saved(self, get_connection):
        connection = FakeConnection()
        get_connection.return_value = connection

        response = self.client.post(
            "/api/reservations", json=self.valid_reservation()
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(connection.committed)
        self.assertIn("INSERT INTO reservations", connection.reservation_cursor.query)
        self.assertEqual(connection.reservation_cursor.params[4], "19:00")


if __name__ == "__main__":
    unittest.main()
