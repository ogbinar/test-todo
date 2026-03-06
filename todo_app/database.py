"""Database module for Todo App"""

import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any
import os

@contextmanager
def get_db():
    """Context manager for database connections"""
    # set to /data/sqlite/test-todo/ in prod
    DB_PATH = os.getenv("SQLITE_PATH", "todo.db")
    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    """Initialize the database with todos table"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def get_all_todos() -> List[Dict[str, Any]]:
    """Get all todos ordered by creation date"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]


def create_todo(task: str) -> Dict[str, Any]:
    """Create a new todo"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (task, completed) VALUES (?, 0)",
            (task,)
        )
        todo_id = cursor.lastrowid
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        return dict(cursor.fetchone())


def update_todo(todo_id: int, completed: bool) -> Dict[str, Any] | None:
    """Update a todo's completion status"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET completed = ? WHERE id = ?",
            (completed, todo_id)
        )
        if cursor.rowcount == 0:
            return None
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        return dict(cursor.fetchone())


def delete_todo(todo_id: int) -> bool:
    """Delete a todo"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        return cursor.rowcount > 0

def update_todo_task(todo_id: int, task: str) -> Dict[str, Any] | None:
    """Update a todo's task field"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET task = ? WHERE id = ?",
            (task, todo_id)
        )
        if cursor.rowcount == 0:
            return None
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        return dict(cursor.fetchone())