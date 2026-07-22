from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LearningCreate(BaseModel):
    project: str
    category: str
    outline: str = None
    estimated_duration: int = 0
    accumulated_duration: int = 0
    progress: int = 0
    start_date: str


class LearningUpdate(BaseModel):
    project: str = None
    category: str = None
    outline: str = None
    estimated_duration: int = None
    accumulated_duration: int = None
    progress: int = None
    start_date: str = None


class LearningOut(BaseModel):
    id: int
    user_id: int
    project: str
    category: str
    outline: str = None
    estimated_duration: int
    accumulated_duration: int
    progress: int
    start_date: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
