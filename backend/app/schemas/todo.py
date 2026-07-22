from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoCreate(BaseModel):
    title: str
    content: Optional[str] = None
    priority: int = 1
    date: str
    completed: bool = False
    start_time: Optional[str] = None
    duration: Optional[int] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = None
    date: Optional[str] = None
    start_time: Optional[str] = None
    duration: Optional[int] = None


class TodoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: Optional[str]
    completed: bool
    priority: int
    date: str
    start_time: Optional[str] = None
    duration: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
