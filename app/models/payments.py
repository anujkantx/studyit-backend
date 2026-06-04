from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
from enum import Enum as PyEnum

class PaymentStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class PaymentProvider(str, PyEnum):
    STRIPE = "stripe"
    PAYPAL = "paypal"
    COUPANCODE = "coupancode"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    discount_code = Column(String, nullable=True)
    final_amount = Column(Float, nullable=False)
    refund_amount = Column(Float, nullable=True)
    currency = Column(String(10), nullable=False)
    payment_gateway = Column(String(50), nullable=False)
    payment_method = Column(String(50), nullable=False)
    gateway_order_id = Column(String, nullable=True)
    gateway_payment_id = Column(String, nullable=True)
    transaction_id = Column(String, nullable=True)
    invoice_number = Column(String, nullable=True)
    webhook_verified = Column(Boolean, default=False, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    gateway_response = Column(String, nullable=True)
    refunded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")
    subscription = relationship("Subscription", back_populates="payments")