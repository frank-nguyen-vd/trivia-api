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

    # DONE: write test cases for endpoint /categories
    def test_get_paginated_categories(self):
        res = self.client().get(
            self.config["api_url"]["base"] + self.config["api_url"]["categories"]
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual("categories" in data, True)

    def test_404_get_categories_beyong_valid_pages(self):
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

    # DONE: write test cases for endpoint /questions
    def test_get_paginated_questions(self):
        res = self.client().get(
            self.config["api_url"]["base"] + self.config["api_url"]["questions"]
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual("questions" in data, True)

    def test_404_get_questions_beyond_valid_pages(self):
        res = self.client().get(
            self.config["api_url"]["base"]
            + self.config["api_url"]["questions"]
            + "?page=100000"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        self.assertEqual("questions" in data, False)

    # DONE: write test cases for /api/v1/quizzes
    def test_get_a_quiz_question(self):
        previous_questions = [1, 2]
        category_id = 1
        res = self.client().post(
            self.config["api_url"]["base"] + self.config["api_url"]["quizzes"],
            json={
                "previous_questions": previous_questions,
                "quiz_category": {"id": category_id},
            },
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual("question" in data, True)
        self.assertEqual("id" in data["question"], True)
        self.assertEqual("question" in data["question"], True)
        self.assertEqual("answer" in data["question"], True)
        self.assertEqual("difficulty" in data["question"], True)
        self.assertEqual("category" in data["question"], True)
        self.assertEqual(data["question"]["id"] in previous_questions, False)
        self.assertEqual(data["question"]["category"], category_id)

    def test_422_send_invalid_filter_for_quiz_question(self):
        # None Type
        res = self.client().post(
            self.config["api_url"]["base"] + self.config["api_url"]["quizzes"],
            json={"previous_questions": None, "quiz_category": None},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable entity")
        self.assertEqual("question" in data, False)

        # Wrong key name
        res = self.client().post(
            self.config["api_url"]["base"] + self.config["api_url"]["quizzes"],
            json={"wrong_previous_questions": [], "wrong_quiz_category": {"id": 1}},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable entity")
        self.assertEqual("question" in data, False)

    # TODO write test cases for /api/v1/category/<int:category_id>/questions
    def test_get_questions_in_category(self):
        res = self.client().post(
            self.config["api_url"]["base"]
            + self.config["api_url"]["categories"]
            + "/1"
            + self.config["api_url"]["questions"]
            + "?page=1"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual("total_questions" in data, True)
        self.assertEqual("questions" in data, True)
        self.assertEqual("current_category" in data, True)

    def test_404_get_categorized_questions_beyond_valid_pages(self):
        res = self.client().post(
            self.config["api_url"]["base"]
            + self.config["api_url"]["categories"]
            + "/1"
            + self.config["api_url"]["questions"]
            + "?page=10000"
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        self.assertEqual("total_questions" in data, False)
        self.assertEqual("questions" in data, False)
        self.assertEqual("current_category" in data, False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()