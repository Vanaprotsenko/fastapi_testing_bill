from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal

from app import models, schemas
from app.api import deps
from app.db.session import get_db
from app.services import receipt as receipt_service
from app.config import settings

router = APIRouter()


@router.post("/", response_model=schemas.ReceiptResponse)
def create_receipt(
        receipt_in: schemas.ReceiptCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Create a new receipt.
    """
    receipt = receipt_service.create_receipt(db, receipt_in, current_user)
    return receipt_service.to_receipt_response(receipt)


@router.get("/", response_model=List[schemas.ReceiptResponse])
def list_receipts(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(deps.get_current_user),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_total: Optional[Decimal] = None,
        max_total: Optional[Decimal] = None,
        payment_type: Optional[schemas.PaymentType] = None,
) -> Any:
    """
    Retrieve receipts for the current user with filtering and pagination.
    """
    receipts = receipt_service.get_user_receipts(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        min_total=min_total,
        max_total=max_total,
        payment_type=payment_type
    )
    return [receipt_service.to_receipt_response(receipt) for receipt in receipts]


@router.get("/{receipt_id}", response_model=schemas.ReceiptResponse)
def get_receipt(
        receipt_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Get a specific receipt by ID.
    """
    receipt = receipt_service.get_receipt(db, receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    if receipt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this receipt"
        )
    return receipt_service.to_receipt_response(receipt)


@router.get("/{receipt_id}/text")
def get_receipt_text(
        receipt_id: int,
        line_width: int = Query(settings.DEFAULT_RECEIPT_LINE_WIDTH, ge=20, le=80),
        db: Session = Depends(get_db)
) -> Any:
    """
    Get a text representation of a receipt by ID.
    This endpoint is publicly accessible.
    """
    receipt = receipt_service.get_receipt(db, receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )

    # Format receipt as text
    receipt_text = receipt_service.format_receipt_as_text(receipt, line_width)
    return {"text": receipt_text}