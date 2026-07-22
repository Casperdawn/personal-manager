from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WeightLossCreate(BaseModel):
    date: str
    weight: float
    height: Optional[float] = 170.0


class WeightLossUpdate(BaseModel):
    date: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None


class WeightLossOut(BaseModel):
    id: int
    user_id: int
    date: str
    weight: float
    height: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
