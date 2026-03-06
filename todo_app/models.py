"""Pydantic models for Todo App"""

from pydantic import BaseModel
from typing import List


class TodoCreate(BaseModel):
    """Model for creating a new todo"""
    task: str


class TodoUpdate(BaseModel):
    """Model for updating a todo"""
    completed: bool

class TodoTaskUpdate(BaseModel):
    """Model for updating a todo's task field"""
    task: str


class TodoResponse(BaseModel):
    """Model for todo response"""
    id: int
    task: str
    completed: bool
    created_at: str


class TodoListResponse(BaseModel):
    """Model for list of todos response"""
    todos: List[TodoResponse]