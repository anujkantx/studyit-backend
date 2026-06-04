from app.db.base import Base

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum





class UserStatus(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    DELETED = "deleted"

class UserRole(str, PyEnum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    phone = Column(String(20), unique=True, nullable=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)

    password_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    role = relationship("Role", back_populates="users") 
    # subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    # uploaded_resources = relationship("Resource", back_populates="uploader", foreign_keys="[Resource.uploaded_by]")
    # approved_resources = relationship("Resource", back_populates="approver", foreign_keys="[Resource.approved_by]")
    # quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    # payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), default=UserRole.STUDENT.value, nullable=False, unique=True)

    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="role")