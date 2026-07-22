from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models.user import User
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.routes.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=list[TodoResponse])
def get_todos(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    priority: Optional[int] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Todo).filter(Todo.user_id == current_user.id)
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    if priority is not None:
        query = query.filter(Todo.priority == priority)
    if year is not None:
        query = query.filter(Todo.date.like(f"{year}-%"))
    if month is not None:
        query = query.filter(Todo.date.like(f"%-{month:02d}-%"))
    if day is not None:
        query = query.filter(Todo.date.like(f"%-{day:02d}"))
    todos = query.order_by(Todo.date.desc(), Todo.created_at.desc()).offset(skip).limit(limit).all()
    return todos


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_todo = Todo(
        user_id=current_user.id,
        title=todo.title,
        content=todo.content,
        priority=todo.priority,
        date=todo.date,
        completed=todo.completed,
        start_time=todo.start_time,
        duration=todo.duration,
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.content is not None:
        todo.content = todo_update.content
    if todo_update.completed is not None:
        todo.completed = todo_update.completed
    if todo_update.priority is not None:
        todo.priority = todo_update.priority
    if todo_update.date is not None:
        todo.date = todo_update.date
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == current_user.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
