# Backend - Full Stack Trivia API

## Introduction

## Getting Started

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

4. **Key Dependencies**

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is an extension that handles SQLAlchemy database migrations for Flask application using Alembic.

### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
sudo -u postgres psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server in development mode, execute:

```bash
export FLASK_APP=flaskr
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Reference

GET `/api/v1/`

- Description: Return a welcome message
- Request Arguments: None
- Returns: An object with a welcome message

```json
{
  "success": True,
  "message": "Welcome to Trivia-Api"
}
```

GET `/api/v1/categories?page=<page_number>`

- Description: Get a paginated list of categories
- Request Arguments:
  - page: if list of categories spans over multiple pages, then `page` is the page number you want to view
- Returns: An object with a key 'categories' that contains objects of key:value pairs.

```json
{
  "success": True,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

GET `/api/v1/questions?page=<number>&searchTerm=<string>`

- Description: Get a paginated list of questions
- Request Arguments:
  - page: if list of questions spans over multiple pages, then `page` is the page number you want to view
  - searchTerm: to find questions that include the string search term
- Returns:

```json
{
  "success": True,
  "total_questions": 2,
  "questions": [
    {
      "id": 1,
      "question": "What is the name of your cat?",
      "answer": "Soloha",
      "category": 1,
      "difficulty": 3
    },
    {
      "id": 1,
      "question": "What is the name of your dog?",
      "answer": "Aloha",
      "category": 1,
      "difficulty": 3
    }
  ],
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 1
}
```

GET `/api/v1/categories/<category_id>/questions?page=<page_number>`

- Description: Get a paginated list of questions in a given category
- Request Arguments:
  - page: if list of questions spans over multiple pages, then `page` is the page number you want to view
- Returns:

```json
{
  "success": True,
  "total_questions": 2,
  "questions": [
    {
      "id": 1,
      "question": "What is the name of your cat?",
      "answer": "Soloha",
      "category": 1,
      "difficulty": 3
    },
    {
      "id": 1,
      "question": "What is the name of your dog?",
      "answer": "Aloha",
      "category": 1,
      "difficulty": 3
    }
  ],
  "current_category": {
    "id": 1
  }
}
```

POST '/api/v1/quizzes'

- Description: Get a random question given a category and previous asked questions
- Request Arguments:

```json
{
  "previous_questions": [1, 3, 5],
  "quiz_category": {
    "id": 1
  }
}
```

- Returns:

```json
{
  "success": True,
  "question": {
    "id": 1,
    "question": "What is the name of your cat?",
    "answer": "Soloha",
    "category": 1,
    "difficulty": 3
  }
}
```

POST '/api/v1/questions'

- Description: Add a new question to database
- Request Arguments:

```json
{
  "question": "Who invented relativity theory?",
  "answer": "Albert Einstein",
  "difficulty": 1,
  "category": 1
}
```

- Returns:

```json
{
  "success": True
}
```

DELETE `/api/v1/questions/<id>`

- Description: Delete a question given id
- Request Arguments: None
- Returns:

```json
{
  "success": True
}
```

## Errors

| Code | Type          | Message               |
| ---- | ------------- | --------------------- |
| 400  | Client errors | Bad request           |
| 404  | Client errors | Resource not found    |
| 500  | Server errors | Internal server error |

## ToDo Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
