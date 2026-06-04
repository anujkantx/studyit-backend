from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Enum, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


class SubscriptionStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    INACTIVE = "INACTIVE"

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    plan_variant_id = Column(Integer, ForeignKey("plan_variants.id"), nullable=False, index=True)
    access_program_id = Column(Integer, ForeignKey("access_programs.id"), nullable=True, index=True)
    status = Column(Enum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.ACTIVE)
    start_at = Column(DateTime, nullable=False)
    expire_at = Column(DateTime, nullable=True)
    last_switched_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")
    plan_variant = relationship("PlanVariant", back_populates="subscriptions")
    access_program = relationship("AccessProgram", back_populates="subscriptions")


class AccessProgram(Base):
    __tablename__ = "access_programs"

    id = Column(Integer, primary_key=True, index=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False, index=True)
    semester = Column(String(20), nullable=False)