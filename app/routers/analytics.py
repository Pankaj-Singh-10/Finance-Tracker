from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Optional, List
from app import models, schemas

def get_summary(
    db: Session, 
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    query = db.query(models.Transaction).filter(models.Transaction.user_id == user_id)
    
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    
    transactions = query.all()
    
    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expenses = sum(t.amount for t in transactions if t.type == "expense")
    
    return schemas.SummaryResponse(
        total_income=total_income,
        total_expenses=total_expenses,
        balance=total_income - total_expenses,
        total_transactions=len(transactions),
        period_start=start_date,
        period_end=end_date
    )

def get_category_breakdown(
    db: Session, 
    user_id: int,
    type: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    query = db.query(
        models.Transaction.category,
        func.sum(models.Transaction.amount).label('total')
    ).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.type == type
    )
    
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    
    results = query.group_by(models.Transaction.category).all()
    
    total = sum(r.total for r in results)
    
    return [
        schemas.CategoryBreakdown(
            category=r.category,
            total=r.total,
            percentage=(r.total / total * 100) if total > 0 else 0
        )
        for r in results
    ]

def get_monthly_summary(
    db: Session, 
    user_id: int,
    months: int = 6
):
    # Get transactions from last N months
    start_date = datetime.utcnow() - timedelta(days=months * 30)
    
    transactions = db.query(models.Transaction).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.date >= start_date
    ).all()
    
    monthly_data = {}
    
    for transaction in transactions:
        month_key = transaction.date.strftime("%Y-%m")
        
        if month_key not in monthly_data:
            monthly_data[month_key] = {"income": 0, "expenses": 0}
        
        if transaction.type == "income":
            monthly_data[month_key]["income"] += transaction.amount
        else:
            monthly_data[month_key]["expenses"] += transaction.amount
    
    # Sort by month
    sorted_months = sorted(monthly_data.keys())
    
    return [
        schemas.MonthlySummary(
            month=month,
            income=data["income"],
            expenses=data["expenses"],
            balance=data["income"] - data["expenses"]
        )
        for month, data in monthly_data.items()
    ][-months:]  # Return last N months

