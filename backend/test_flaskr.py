import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


def load_config():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(file_dir, "flaskr/config.json")
    with open(file_path) as f:
        config = json.load(f)
    return config


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    config = load_config()

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            "postgres", "postgres", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO: Write at least one test for each test for successful operation and for expected errors.
    """

    # TODO: write test cases for endpoint /categories
    def test_get_paginated_categories(self):
        res = self.client().get(
            self.config["api_url"]["base"] + self.config["api_url"]["categories"]
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual("categories" in data, True)

    def test_404_request_categories_beyong_valid_pages(self):
        res = self.client().get(
            self.config["api_url"]["base"]
            + self.config["api_url"]["categories"]
            + "?page=100000"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        self.assertEqual("categories" in data, False)

    # TODO: write test cases for /api/v1/questions

    # TODO: write test cases for /api/v1/quizzes


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()