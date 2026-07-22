from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models.user import User
from app.models.learning import Learning
from app.schemas.learning import LearningCreate, LearningUpdate, LearningOut
from app.routes.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=list[LearningOut])
def get_learning(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Learning).filter(Learning.user_id == current_user.id)
    if category is not None:
        query = query.filter(Learning.category == category)
    records = query.offset(skip).limit(limit).all()
    return records


@router.get("/{learning_id}", response_model=LearningOut)
def get_learning_by_id(
    learning_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(Learning).filter(Learning.id == learning_id, Learning.user_id == current_user.id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Learning record not found")
    return record


@router.post("/", response_model=LearningOut, status_code=status.HTTP_201_CREATED)
def create_learning(
    learning: LearningCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_learning = Learning(
        user_id=current_user.id,
        project=learning.project,
        category=learning.category,
        outline=learning.outline,
        estimated_duration=learning.estimated_duration,
        accumulated_duration=learning.accumulated_duration,
        progress=learning.progress,
        start_date=learning.start_date,
    )
    db.add(new_learning)
    db.commit()
    db.refresh(new_learning)
    return new_learning


@router.put("/{learning_id}", response_model=LearningOut)
def update_learning(
    learning_id: int,
    learning_update: LearningUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(Learning).filter(Learning.id == learning_id, Learning.user_id == current_user.id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Learning record not found")
    if learning_update.project is not None:
        record.project = learning_update.project
    if learning_update.category is not None:
        record.category = learning_update.category
    if learning_update.outline is not None:
        record.outline = learning_update.outline
    if learning_update.estimated_duration is not None:
        record.estimated_duration = learning_update.estimated_duration
    if learning_update.accumulated_duration is not None:
        record.accumulated_duration = learning_update.accumulated_duration
    if learning_update.progress is not None:
        record.progress = learning_update.progress
    if learning_update.start_date is not None:
        record.start_date = learning_update.start_date
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{learning_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_learning(
    learning_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(Learning).filter(Learning.id == learning_id, Learning.user_id == current_user.id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Learning record not found")
    db.delete(record)
    db.commit()
