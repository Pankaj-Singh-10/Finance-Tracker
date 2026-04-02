from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app import schemas, analytics, auth
from app.database import get_db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary", response_model=schemas.SummaryResponse)
def get_summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """Get financial summary (All authenticated users)"""
    return analytics.get_summary(
        db, current_user.id, start_date, end_date
    )

@router.get("/category-breakdown/{type}", response_model=List[schemas.CategoryBreakdown])
def get_category_breakdown(
    type: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """Get category breakdown for income or expenses (All authenticated users)"""
    if type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Type must be 'income' or 'expense'")
    
    return analytics.get_category_breakdown(
        db, current_user.id, type, start_date, end_date
    )

@router.get("/monthly", response_model=List[schemas.MonthlySummary])
def get_monthly_summary(
    months: int = Query(6, ge=1, le=24),
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """Get monthly summary for last N months (All authenticated users)"""
    return analytics.get_monthly_summary(db, current_user.id, months)

    