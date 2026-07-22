from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import Optional
from app.core.database import get_db
from app.models.user import User
from app.models.finance import Finance
from app.schemas.finance import FinanceCreate, FinanceUpdate, FinanceOut
from app.routes.auth import get_current_user

router = APIRouter()


@router.get("/years")
def get_available_years(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    years = db.query(
        func.substr(Finance.date, 1, 4).label('year')
    ).filter(
        Finance.user_id == current_user.id
    ).group_by('year').order_by('year').all()
    
    year_list = [int(row.year) for row in years]
    
    return {"years": sorted(year_list)}


@router.get("/wallet")
def get_wallet(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_income = db.query(func.sum(Finance.amount)).filter(
        Finance.user_id == current_user.id,
        Finance.type == "income"
    ).scalar() or 0.0

    total_expense = db.query(func.sum(Finance.amount)).filter(
        Finance.user_id == current_user.id,
        Finance.type == "expense"
    ).scalar() or 0.0

    normal_categories = ["餐饮", "交通", "教育", "医疗", "房租"]
    comfort_categories = ["购物", "娱乐"]
    irrational_categories = ["其他支出"]

    normal_expense = db.query(func.sum(Finance.amount)).filter(
        Finance.user_id == current_user.id,
        Finance.type == "expense",
        Finance.category.in_(normal_categories)
    ).scalar() or 0.0

    comfort_expense = db.query(func.sum(Finance.amount)).filter(
        Finance.user_id == current_user.id,
        Finance.type == "expense",
        Finance.category.in_(comfort_categories)
    ).scalar() or 0.0

    irrational_expense = db.query(func.sum(Finance.amount)).filter(
        Finance.user_id == current_user.id,
        Finance.type == "expense",
        Finance.category.in_(irrational_categories)
    ).scalar() or 0.0

    balance = total_income - total_expense

    return {
        "balance": round(balance, 2),
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "normal_expense": round(normal_expense, 2),
        "comfort_expense": round(comfort_expense, 2),
        "irrational_expense": round(irrational_expense, 2)
    }


@router.get("/monthly-stats")
def get_monthly_stats(
    year: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if year is None:
        year = func.extract('year', func.now())
    
    monthly_data = db.query(
        extract('month', func.strftime('%Y-%m-%d', Finance.date)).label('month'),
        func.sum(Finance.amount).filter(Finance.type == 'income').label('income'),
        func.sum(Finance.amount).filter(Finance.type == 'expense').label('expense'),
    ).filter(
        Finance.user_id == current_user.id,
        func.strftime('%Y', Finance.date) == str(year) if isinstance(year, int) else func.extract('year', func.strftime('%Y-%m-%d', Finance.date)) == year
    ).group_by('month').order_by(extract('month', func.strftime('%Y-%m-%d', Finance.date)).desc()).all()

    result = []
    for row in monthly_data:
        income = float(row.income) if row.income else 0.0
        expense = float(row.expense) if row.expense else 0.0
        result.append({
            "month": int(row.month),
            "income": round(income, 2),
            "expense": round(expense, 2),
            "balance": round(income - expense, 2)
        })
    return result


@router.get("/daily-stats/{year}/{month}")
def get_daily_stats(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    daily_data = db.query(
        extract('day', func.strftime('%Y-%m-%d', Finance.date)).label('day'),
        func.sum(Finance.amount).filter(Finance.type == 'income').label('income'),
        func.sum(Finance.amount).filter(Finance.type == 'expense').label('expense'),
    ).filter(
        Finance.user_id == current_user.id,
        func.strftime('%Y', Finance.date) == str(year),
        func.strftime('%m', Finance.date) == f"{month:02d}"
    ).group_by('day').order_by(extract('day', func.strftime('%Y-%m-%d', Finance.date)).desc()).all()

    result = []
    for row in daily_data:
        income = float(row.income) if row.income else 0.0
        expense = float(row.expense) if row.expense else 0.0
        result.append({
            "date": f"{year}-{month:02d}-{int(row.day):02d}",
            "day": int(row.day),
            "income": round(income, 2),
            "expense": round(expense, 2),
            "balance": round(income - expense, 2)
        })
    return result


@router.get("/daily-details/{date}")
def get_daily_details(
    date: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = db.query(Finance).filter(
        Finance.user_id == current_user.id,
        Finance.date == date
    ).order_by(Finance.created_at.desc()).all()
    
    total_income = sum(r.amount for r in records if r.type == 'income')
    total_expense = sum(r.amount for r in records if r.type == 'expense')
    
    return {
        "date": date,
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "balance": round(total_income - total_expense, 2),
        "records": records
    }


@router.get("/", response_model=list[FinanceOut])
def get_finance(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Finance).filter(Finance.user_id == current_user.id)
    if type is not None:
        query = query.filter(Finance.type == type)
    if date is not None:
        query = query.filter(Finance.date == date)
    records = query.offset(skip).limit(limit).all()
    return records


@router.get("/{finance_id}", response_model=FinanceOut)
def get_finance_by_id(
    finance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(Finance).filter(Finance.id == finance_id, Finance.user_id == current_user.id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Finance record not found")
    return record


@router.post("/", response_model=FinanceOut, status_code=status.HTTP_201_CREATED)
def create_finance(
    finance: FinanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_finance = Finance(
        user_id=current_user.id,
        type=finance.type,
        category=finance.category,
        amount=finance.amount,
        description=finance.description,
        date=finance.date,
    )
    db.add(new_finance)
    
    if finance.type == "income":
        current_user.balance += finance.amount
    else:
        current_user.balance -= finance.amount
    
    db.commit()
    db.refresh(new_finance)
    db.refresh(current_user)
    return new_finance


@router.put("/{finance_id}", response_model=FinanceOut)
def update_finance(
    finance_id: int,
    finance_update: FinanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(Finance).filter(Finance.id == finance_id, Finance.user_id == current_user.id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Finance record not found")
    
    if finance_update.type is not None and finance_update.type != record.type:
        if record.type == "income":
            current_user.balance -= record.amount
        else:
            current_user.balance += record.amount
        record.type = finance_update.type
        if record.type == "income":
            current_user.balance += record.amount
        else:
            current_user.balance -= record.amount
    
    if finance_update.amount is not None and finance_update.amount != record.amount:
        if record.type == "income":
            current_user.balance += finance_update.amount - record.amount
        else:
            current_user.balance -= finance_update.amount - record.amount
        record.amount = finance_update.amount
    
    if finance_update.category is not None:
        record.category = finance_update.category
    if finance_update.description is not None:
        record.description = finance_update.description
    if finance_update.date is not None:
        record.date = finance_update.date
    
    db.commit()
    db.refresh(record)
    db.refresh(current_user)
    return record


@router.delete("/{finance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_finance(
    finance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = db.query(Finance).filter(Finance.id == finance_id, Finance.user_id == current_user.id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Finance record not found")
    
    if record.type == "income":
        current_user.balance -= record.amount
    else:
        current_user.balance += record.amount
    
    db.delete(record)
    db.commit()
    db.refresh(current_user)
