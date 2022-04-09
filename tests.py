import unittest
import os
import flask
from app import app
from models import db


class GameRecommenderTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        db_url = os.getenv("DATABASE_URL")
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    def tearDown(self):
        pass

    def test_login_page_render(self):
        response = self.app.get("/", follow_redirects=True)
        expected_response = 200
        self.assertEqual(response.status_code, expected_response)

    def test_profile_page_render(self):
        response = self.app.get("/profile", follow_redirects=False)
        expected_response = 200
        self.assertEqual(response.status_code, expected_response)

    def test_signup(self):
        data = dict(
            username="testinguser",
            email="testinguser@gmail.com",
            password="testinguser",
        )
        response = self.app.post("/signup", data=data, follow_redirects=True)
        expected_response = 200
        self.assertEqual(response.status_code, expected_response)

    def test_login(self):
        data = dict(email="abhis", password="abhis")
        response = self.app.post("/login", data=data, follow_redirects=True)
        expected_response = 404
        self.assertEqual(response.status_code, expected_response)


if __name__ == "__main__":
    unittest.main()
