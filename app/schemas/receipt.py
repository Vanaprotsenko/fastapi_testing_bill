from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from decimal import Decimal


class PaymentType(str, Enum):
    CASH = "cash"
    CASHLESS = "cashless"


class ProductBase(BaseModel):
    name: str
    price: Decimal
    quantity: Decimal


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    total: Decimal


class PaymentBase(BaseModel):
    type: PaymentType
    amount: Decimal


class ReceiptCreate(BaseModel):
    products: List[ProductCreate]
    payment: PaymentBase


class ReceiptResponse(BaseModel):
    id: int
    products: List[ProductResponse]
    payment: PaymentBase
    total: Decimal
    rest: Decimal
    created_at: datetime

    class Config:
        orm_mode = True


class ReceiptFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_total: Optional[Decimal] = None
    max_total: Optional[Decimal] = None
    payment_type: Optional[PaymentType] = None


class ReceiptTextParams(BaseModel):
    line_width: Optional[int] = 32