from app.db.base import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    

class plan_variant(Base):
    __tablename__ = "plan_variants"

    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False, index=True)
    duration_months = Column(Integer, nullable=False)
    original_price = Column(Float, nullable=False)
    discounted_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    plan = relationship("Plan", back_populates="plan_variants")

