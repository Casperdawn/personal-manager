from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Learning(Base):
    __tablename__ = "learning"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    outline = Column(String(1000), nullable=True)
    estimated_duration = Column(Integer, default=0)
    accumulated_duration = Column(Integer, default=0)
    progress = Column(Integer, default=0)
    start_date = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
