"""Tests for Todo API endpoints"""

import pytest
from fastapi.testclient import TestClient

from todo_app import app
from todo_app.database import get_db, init_db


@pytest.fixture(autouse=True)
def setup_db():
    """Setup and teardown database for each test"""
    init_db()
    yield
    # Clean up after tests
    with get_db() as conn:
        conn.execute("DELETE FROM todos")


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def sample_todo():
    """Sample todo data"""
    return {"task": "Test task", "completed": False}


class TestRoot:
    """Tests for root endpoint"""

    def test_root(self, client):
        """Test root endpoint returns correct info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data


class TestHealth:
    """Tests for health check endpoint"""

    def test_health_check(self, client):
        """Test health check returns healthy status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestTodos:
    """Tests for todos endpoints"""

    def test_get_todos_empty(self, client):
        """Test getting todos when none exist"""
        response = client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_create_todo(self, client, sample_todo):
        """Test creating a new todo"""
        response = client.post("/api/todos", json=sample_todo)
        assert response.status_code == 201
        data = response.json()
        assert data["task"] == sample_todo["task"]
        assert data["completed"] == False
        assert "id" in data
        assert "created_at" in data

    def test_create_todo_missing_task(self, client):
        """Test creating todo without task raises error"""
        response = client.post("/api/todos", json={"completed": False})
        assert response.status_code == 422

    def test_get_todos_after_create(self, client, sample_todo):
        """Test getting todos after creating one"""
        # Create todo
        create_response = client.post("/api/todos", json=sample_todo)
        created_id = create_response.json()["id"]

        # Get todos
        response = client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == created_id
        assert data[0]["task"] == sample_todo["task"]

    def test_update_todo(self, client, sample_todo):
        """Test updating a todo"""
        # Create todo
        create_response = client.post("/api/todos", json=sample_todo)
        created_id = create_response.json()["id"]

        # Update todo
        update_data = {"completed": True}
        response = client.put(f"/api/todos/{created_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] == True

    def test_update_nonexistent_todo(self, client):
        """Test updating non-existent todo raises error"""
        response = client.put("/api/todos/999", json={"completed": True})
        assert response.status_code == 404

    def test_delete_todo(self, client, sample_todo):
        """Test deleting a todo"""
        # Create todo
        create_response = client.post("/api/todos", json=sample_todo)
        created_id = create_response.json()["id"]

        # Delete todo
        response = client.delete(f"/api/todos/{created_id}")
        assert response.status_code == 204

    def test_delete_nonexistent_todo(self, client):
        """Test deleting non-existent todo raises error"""
        response = client.delete("/api/todos/999")
        assert response.status_code == 404

    def test_get_todos_after_delete(self, client, sample_todo):
        """Test getting todos after deleting one"""
        # Create todo
        create_response = client.post("/api/todos", json=sample_todo)
        created_id = create_response.json()["id"]

        # Delete todo
        client.delete(f"/api/todos/{created_id}")

        # Get todos
        response = client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    def test_multiple_todos(self, client):
        """Test creating and managing multiple todos"""
        # Create multiple todos
        for i in range(3):
            response = client.post("/api/todos", json={"task": f"Task {i}"})
            assert response.status_code == 201

        # Get all todos
        response = client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

        # Complete one todo
        client.put(f"/api/todos/{data[0]['id']}", json={"completed": True})

        # Get todos again
        response = client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["completed"] == True
        assert data[1]["completed"] == False
        assert data[2]["completed"] == False

        # Delete one todo
        client.delete(f"/api/todos/{data[1]['id']}")

        # Get todos again
        response = client.get("/api/todos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2