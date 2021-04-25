import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
from models import setup_db, Question, Category
import os

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

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

    @app.route("/api/v1")
    def index():
        return jsonify({"success": True, "message": "Welcome to Trivia-API"})

    """
    DONE: Create an endpoint to handle GET requests for all available categories.
    """

    def conv_categories_list_to_dict(categories):
        returned_categories = {}
        for category in categories:
            returned_categories[category.id] = category.type
        return returned_categories

    @app.route("/api/v1/categories")
    def find_categories():
        page = request.args.get("page", 1, type=int)
        item_per_page = 10

        try:
            list_of_categories = Category.query.all()
        except:
            abort(500)

        start_index = (page - 1) * item_per_page
        end_index = page * item_per_page

        if start_index > len(list_of_categories):
            abort(404)

        returned_categories = conv_categories_list_to_dict(
            list_of_categories[start_index:end_index]
        )

        return jsonify({"success": True, "categories": returned_categories}), 200

    """
    @DONE: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    """

    """
    @DONE: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    """

    @app.route("/api/v1/questions")
    def find_questions():
        page = request.args.get("page", 1, type=int)
        search_term = request.args.get("searchTerm", "", type=str)
        item_per_page = 5

        try:
            list_of_questions = Question.query.filter(
                Question.question.like("%{}%".format(search_term))
            ).all()
        except:
            abort(500)

        start_index = (page - 1) * item_per_page
        end_index = page * item_per_page

        if start_index > len(list_of_questions):
            abort(404)

        returned_questions = []
        for question in list_of_questions[start_index:end_index]:
            returned_questions.append(question.format())

        try:
            list_of_categories = Category.query.all()
        except:
            abort(500)

        returned_categories = conv_categories_list_to_dict(list_of_categories)

        return jsonify(
            {
                "success": True,
                "total_questions": len(list_of_questions),
                "questions": returned_questions,
                "categories": returned_categories,
            }
        )

    """
    @DONE: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    """

    @app.route("/api/v1/questions/<int:question_id>", methods=["DELETE"])
    def delete_a_question(question_id):
        question = Question.query.get(question_id)

        if question is None:
            abort(404)

        try:
            question.delete()
        except:
            abort(500)

        return jsonify({"success": True})

    """
    @DONE: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    """

    @app.route("/api/v1/questions", methods=["POST"])
    def create_a_question():
        try:
            body = request.get_json()
            question = body.get("question")
            answer = body.get("answer")
            difficulty = body.get("difficulty")
            category = body.get("category")
        except:
            abort(422)

        if question is None or answer is None or difficulty is None or category is None:
            abort(422)

        try:
            new_question = Question(question, answer, category, difficulty)
            new_question.insert()
        except:
            abort(500)

        return jsonify({"success": True})

    """
    @DONE: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    """

    @app.route("/api/v1/categories/<int:category_id>/questions")
    def find_questions_in_category(category_id):
        page = request.args.get("page", 1, type=int)
        item_per_page = 5

        try:
            list_of_questions = Question.query.filter(
                Question.category == category_id
            ).all()
        except:
            abort(500)

        start_index = (page - 1) * item_per_page
        end_index = page * item_per_page

        if start_index > len(list_of_questions):
            abort(404)

        returned_questions = []
        for question in list_of_questions[start_index:end_index]:
            returned_questions.append(question.format())

        return jsonify(
            {
                "success": True,
                "total_questions": len(returned_questions),
                "questions": returned_questions,
                "current_category": category_id,
            }
        )

    """
    @DONE: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    """

    @app.route("/api/v1/quizzes", methods=["POST"])
    def get_a_random_question():
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions")
            quiz_category = body.get("quiz_category")
        except:
            abort(422)

        if previous_questions is None or not isinstance(previous_questions, list):
            abort(422)

        if quiz_category is None:
            abort(422)

        try:
            list_of_questions = Question.query.filter(
                Question.id not in previous_questions,
                Question.category == quiz_category["id"],
            ).all()

            if list_of_questions == []:
                return jsonify({"success": True})

            returned_question = list_of_questions[
                random.randint(0, len(list_of_questions) - 1)
            ].format()
        except:
            abort(500)

        return jsonify(
            {
                "success": True,
                "question": returned_question,
            }
        )

    """
    @DONE: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    """

    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "unprocessable entity"}
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "internal server error"}
            ),
            500,
        )

    return app
