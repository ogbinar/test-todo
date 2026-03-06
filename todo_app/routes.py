"""API routes for Todo App"""

from typing import List

from fastapi import APIRouter, HTTPException

from .database import get_all_todos, create_todo, update_todo, delete_todo
from .models import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter()


@router.get("/todos", response_model=List[TodoResponse])
def get_todos():
    """Get all todos"""
    return get_all_todos()


@router.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo_endpoint(todo: TodoCreate):
    """Create a new todo"""
    return create_todo(todo.task)


@router.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo_endpoint(todo_id: int, todo: TodoUpdate):
    """Update a todo"""
    result = update_todo(todo_id, todo.completed)
    if result is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return result


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo_endpoint(todo_id: int):
    """Delete a todo"""
    if not delete_todo(todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")