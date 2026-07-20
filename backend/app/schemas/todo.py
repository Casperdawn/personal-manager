from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoCreate(BaseModel):
    title: str
    content: Optional[str] = None
    priority: int = 1


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = None


class TodoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: Optional[str]
    completed: bool
    priority: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
