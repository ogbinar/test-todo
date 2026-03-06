#!/usr/bin/env python3
"""Simple Todo App with FastAPI and SQLite"""

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from todo_app.database import init_db
from todo_app.routes import router

app = FastAPI(title="Todo App", version="1.0.0")

# Initialize database
init_db()

# Mount templates
templates = Jinja2Templates(directory="templates")

# Include API router
app.include_router(router, prefix="/api", tags=["todos"])


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)