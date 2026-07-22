from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FinanceCreate(BaseModel):
    type: str
    category: str
    amount: float
    description: str = None
    date: str


class FinanceUpdate(BaseModel):
    type: str = None
    category: str = None
    amount: float = None
    description: str = None
    date: str = None


class FinanceOut(BaseModel):
    id: int
    user_id: int
    type: str
    category: str
    amount: float
    description: str = None
    date: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
