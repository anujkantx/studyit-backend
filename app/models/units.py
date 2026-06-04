from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


class unit(Base):
	__tablename__ = "units"

	id = Column(Integer, primary_key=True, index=True)
	subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
	unit_number = Column(Integer, nullable=False)
	name = Column(String, nullable=False)
	slug = Column(String, nullable=False)
	description = Column(String, nullable=True)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)


class topic(Base):
	__tablename__ = "topics"

	id = Column(Integer, primary_key=True, index=True)
	unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)
	name = Column(String, nullable=False)
	slug = Column(String, nullable=False)
	description = Column(String, nullable=True)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)

