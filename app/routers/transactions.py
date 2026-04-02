from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.check_role(["admin", "analyst"]))
):
    """Create a new transaction (Admin and Analyst only)"""
    return crud.create_transaction(db=db, transaction=transaction, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    type: Optional[str] = Query(None, regex="^(income|expense)$"),
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """Get user's transactions with optional filters (All authenticated users)"""
    return crud.get_transactions(
        db=db, 
        user_id=current_user.id, 
        skip=skip, 
        limit=limit,
        type=type,
        category=category,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    """Get a specific transaction (All authenticated users)"""
    transaction = crud.get_transaction(db, transaction_id=transaction_id, user_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.check_role(["admin", "analyst"]))
):
    """Update a transaction (Admin and Analyst only)"""
    transaction = crud.update_transaction(
        db, transaction_id, transaction_update, current_user.id
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.check_role(["admin"]))
):
    """Delete a transaction (Admin only)"""
    success = crud.delete_transaction(db, transaction_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return None

