from unittest import TestCase

from fastapi.testclient import TestClient

from app import app


class TestApp(TestCase):
    def test_main(self):
        client = TestClient(app)

        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Piccolo + ASGI", response.text)
