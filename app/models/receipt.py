from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base


class PaymentType(str, enum.Enum):
    CASH = "cash"
    CASHLESS = "cashless"


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    products = Column(JSON, nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)
    payment_amount = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    rest_amount = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="receipts")