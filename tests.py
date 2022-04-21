"""Project Testing"""
import unittest
import os
from app import app
from unittest.mock import MagicMock, patch
from steamspy import query_favorites, querygames
from models import Survey


class GameRecommenderTests(unittest.TestCase):
    """Game Recommender Tests"""

    def setUp(self):
        """Configures DB for testing purposes"""
        app.config["TESTING"] = True
        self.app = app.test_client()
        db_url = os.getenv("DATABASE_URL")
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    def tearDown(self):
        """Signifies the end of testing"""
        pass

    def test_login_page_render(self):
        """Asserts that the login page will render"""
        response = self.app.get("/", follow_redirects=True)
        expected_response = 200
        self.assertEqual(response.status_code, expected_response)

    def test_profile_page_render(self):
        """Asserts that a users profile page will render"""
        response = self.app.get("/profile", follow_redirects=False)
        expected_response = 302
        self.assertEqual(response.status_code, expected_response)

    def test_signup(self):
        """Asserts that a user can successfully register to the site"""
        data = dict(
            username="testinguser",
            email="testinguser@gmail.com",
            password="testinguser",
        )
        response = self.app.post("/signup", data=data, follow_redirects=True)
        expected_response = 200
        self.assertEqual(response.status_code, expected_response)

    def test_login(self):
        """Asserts that a current user can successfully log in to the site"""
        data = dict(email="good@email.com", password="good")
        response = self.app.post("/login", data=data, follow_redirects=True)
        expected_response = 200
        self.assertEqual(response.status_code, expected_response)

    def test_query_favorites(self):
        """Asserts that query_favorites will process a list of game ids correctly"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "appid": 1089350,
            "name": "NBA 2K20",
            "developer": "Visual Concepts",
            "publisher": "2K",
            "score_rank": "",
            "positive": 30512,
            "negative": 30076,
            "userscore": 0,
            "owners": "5,000,000 .. 10,000,000",
            "average_forever": 8607,
            "average_2weeks": 50,
            "median_forever": 3935,
            "median_2weeks": 50,
            "price": "0",
            "initialprice": "0",
            "discount": "0",
            "ccu": 2006,
            "languages": "English, French, Italian, German, Spanish - Spain, Japanese, Korean, Simplified Chinese, Traditional Chinese",
            "genre": "Simulation, Sports",
            "tags": {
                "Basketball": 292,
                "Sports": 184,
                "Simulation": 125,
                "Multiplayer": 111,
                "Singleplayer": 49,
                "Capitalism": 37,
                "Loot": 22,
                "Casual": 20,
                "Local Multiplayer": 16,
                "Massively Multiplayer": 14,
                "Character Customization": 14,
                "Controller": 14,
                "Realistic": 11,
            },
        }

        with patch("steamspy.requests.get") as mock_requests_get:
            mock_requests_get.return_value = mock_response

            self.assertEqual(query_favorites([1089350])[0]["title"], "NBA 2K20")

    def test_query_favorites_fail(self):
        """Asserts that the previous test will fail given incorrect data"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "appid": 1089350,
            "name": "not NBA 2K20",
            "developer": "Visual Concepts",
            "publisher": "2K",
            "score_rank": "",
            "positive": 30512,
            "negative": 30076,
            "userscore": 0,
            "owners": "5,000,000 .. 10,000,000",
            "average_forever": 8607,
            "average_2weeks": 50,
            "median_forever": 3935,
            "median_2weeks": 50,
            "price": "0",
            "initialprice": "0",
            "discount": "0",
            "ccu": 2006,
            "languages": "English, French, Italian, German, Spanish - Spain, Japanese, Korean, Simplified Chinese, Traditional Chinese",
            "genre": "Simulation, Sports",
            "tags": {
                "Basketball": 292,
                "Sports": 184,
                "Simulation": 125,
                "Multiplayer": 111,
                "Singleplayer": 49,
                "Capitalism": 37,
                "Loot": 22,
                "Casual": 20,
                "Local Multiplayer": 16,
                "Massively Multiplayer": 14,
                "Character Customization": 14,
                "Controller": 14,
                "Realistic": 11,
            },
        }

        with patch("steamspy.requests.get") as mock_requests_get:
            mock_requests_get.return_value = mock_response

            self.assertNotEqual(query_favorites([1089350])[0]["title"], "NBA 2K20")


if __name__ == "__main__":
    unittest.main()
