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


class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), default=UserRole.STUDENT.value, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    avatar_url = Column(String(500), nullable=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, index=True)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE, nullable=False)

    password_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    role = relationship("Role", back_populates="users")
    student_profile = relationship("StudentProfile", back_populates="user", uselist=False) 

    refresh_sessions = relationship("RefreshSession", back_populates="user", cascade="all, delete-orphan")
    # subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    # uploaded_resources = relationship("Resource", back_populates="uploader", foreign_keys="[Resource.uploaded_by]")
    # approved_resources = relationship("Resource", back_populates="approver", foreign_keys="[Resource.approved_by]")
    # quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    # payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    university = Column(String(255), nullable=True)
    college = Column(String(255), nullable=True)
    branch = Column(String(255), nullable=True)
    program = Column(String(255), nullable=True)
    admission_year = Column(Integer, nullable=True)
    graduation_year = Column(Integer, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_completed = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    user = relationship("User", back_populates="student_profile")


class RefreshSession(Base):
    __tablename__ = "refresh_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    refresh_token_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="refresh_sessions")

    