import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to My DevOps Portfolio", response.data)

    def test_about_page(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"About Me", response.data)

if __name__ == "__main__":
    unittest.main()
