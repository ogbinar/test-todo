# Todo App

A simple, minimal todo application built with FastAPI and SQLite.

## Features

- ✅ Create, read, update, and delete todos
- ✅ Beautiful, responsive web UI
- ✅ RESTful API with interactive documentation
- ✅ SQLite database for persistence
- ✅ Comprehensive test suite

## Project Structure

```
.
├── todo_app/
│   ├── __init__.py
│   ├── database.py      # Database operations
│   ├── models.py        # Pydantic models
│   ├── routes.py        # API routes
│   └── todo_app.py      # FastAPI application
├── templates/
│   └── index.html       # Frontend UI
├── tests/
│   ├── __init__.py
│   └── test_api.py      # API tests
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python todo_app.py
```

The app will start on `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main page with UI |
| GET | `/health` | Health check |
| GET | `/api/todos` | List all todos |
| POST | `/api/todos` | Create a new todo |
| PUT | `/api/todos/{id}` | Update a todo |
| DELETE | `/api/todos/{id}` | Delete a todo |

## Interactive Documentation

Visit `/docs` for interactive API documentation (Swagger UI)

## Running Tests

```bash
pytest
```

## Technologies Used

- FastAPI - Web framework
- SQLite - Database
- Jinja2 - Template engine
- Pydantic - Data validation
- pytest - Testing framework