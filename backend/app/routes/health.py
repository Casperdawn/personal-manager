from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.health import WeightLoss
from app.schemas.health import WeightLossCreate, WeightLossUpdate, WeightLossOut
from app.routes.auth import get_current_user

router = APIRouter()


@router.get("/weight-loss/", response_model=list[WeightLossOut])
def get_weight_loss(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = db.query(WeightLoss).filter(
        WeightLoss.user_id == current_user.id
    ).order_by(WeightLoss.date.desc()).offset(skip).limit(limit).all()
    return records


@router.get("/weight-loss/{record_id}", response_model=WeightLossOut)
def get_weight_loss_by_id(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(WeightLoss).filter(
        WeightLoss.id == record_id, WeightLoss.user_id == current_user.id
    ).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Weight loss record not found")
    return record


@router.post("/weight-loss/", response_model=WeightLossOut, status_code=status.HTTP_201_CREATED)
def create_weight_loss(
    record: WeightLossCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_record = WeightLoss(
        user_id=current_user.id,
        date=record.date,
        weight=record.weight,
        height=record.height,
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.put("/weight-loss/{record_id}", response_model=WeightLossOut)
def update_weight_loss(
    record_id: int,
    record_update: WeightLossUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(WeightLoss).filter(
        WeightLoss.id == record_id, WeightLoss.user_id == current_user.id
    ).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Weight loss record not found")
    if record_update.date is not None:
        record.date = record_update.date
    if record_update.weight is not None:
        record.weight = record_update.weight
    if record_update.height is not None:
        record.height = record_update.height
    db.commit()
    db.refresh(record)
    return record


@router.delete("/weight-loss/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weight_loss(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(WeightLoss).filter(
        WeightLoss.id == record_id, WeightLoss.user_id == current_user.id
    ).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Weight loss record not found")
    db.delete(record)
    db.commit()
