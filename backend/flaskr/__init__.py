import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
from models import setup_db, Question, Category
import os

QUESTIONS_PER_PAGE = 10


def load_config():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(file_dir, "config.json")
    with open(file_path) as f:
        config = json.load(f)
    return config


def create_app(test_config=None):
    # create and configure the app
    config = load_config()

    app = Flask(__name__)
    setup_db(app)
    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(
        app, resources={r"{}/*".format(config["api_url"]["base"]): {"origins": "*"}}
    )

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    @app.route(config["api_url"]["base"])
    def index():
        return jsonify({"success": True, "message": "Welcome to Trivia-API"})

    """
    DONE: Create an endpoint to handle GET requests for all available categories.
    """

    @app.route(config["api_url"]["base"] + config["api_url"]["categories"])
    def find_categories():
        try:
            page = request.args.get("page", 1, type=int)
            item_per_page = 10

            list_of_categories = Category.query.all()

            start_index = (page - 1) * item_per_page
            end_index = page * item_per_page

            if start_index > len(list_of_categories):
                abort(404)

            returned_categories = {}
            for category in list_of_categories[start_index:end_index]:
                returned_categories[category.id] = category.type

        except:
            abort(500)

        return jsonify({"success": True, "categories": returned_categories}), 200

    """
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    """

    @app.route(config["api_url"]["base"] + config["api_url"]["questions"])
    def find_questions():
        return jsonify(
            {
                "success": True,
                "total_questions": 2,
                "questions": [
                    {
                        "id": 1,
                        "question": "What is the name of your cat?",
                        "answer": "Soloha",
                        "category": 1,
                        "difficulty": 3,
                    },
                    {
                        "id": 1,
                        "question": "What is the name of your dog?",
                        "answer": "Aloha",
                        "category": 1,
                        "difficulty": 3,
                    },
                ],
                "categories": {
                    "1": "Science",
                    "2": "Art",
                    "3": "Geography",
                    "4": "History",
                    "5": "Entertainment",
                    "6": "Sports",
                },
                "current_category": "Art",
            }
        )

    """
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    """

    """
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    """

    """
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    """

    """
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    """

    """
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    """

    """
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    """

    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "internal server error"}
            ),
            404,
        )

    return app
