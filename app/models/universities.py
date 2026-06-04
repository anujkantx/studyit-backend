from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.database import Base


class University(Base):
	__tablename__ = "universities"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, nullable=False)
	slug = Column(String, unique=True, nullable=False)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)


class Program(Base):
	__tablename__ = "programs"

	id = Column(Integer, primary_key=True, index=True)
	university_id = Column(Integer, ForeignKey("universities.id"), nullable=False, index=True)
	name = Column(String, nullable=False)
	slug = Column(String, nullable=False)
	duration_years = Column(Integer, nullable=False)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)

	university = relationship("University", back_populates="programs")
	
class subject(Base):
	__tablename__ = "subjects"

	id = Column(Integer, primary_key=True, index=True)
	code = Column(String, nullable=False)
	name = Column(String, nullable=False)
	slug = Column(String, nullable=False)
	subject_type = Column(String, nullable=False)
	description = Column(String, nullable=True)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)

class program_subject(Base):
	__tablename__ = "program_subjects"

	id = Column(Integer, primary_key=True, index=True)
	program_id = Column(Integer, ForeignKey("programs.id"), nullable=False, index=True)
	subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
	semester = Column(String(20), nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)

	program = relationship("Program", back_populates="subjects")
	subject = relationship("Subject", back_populates="programs")


