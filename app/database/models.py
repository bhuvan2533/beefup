from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Text
from app.database.dbSession import Base
from datetime import datetime, timezone

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class Company(Base, TimestampMixin):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    employees = relationship("EmployeeProfile", back_populates="company")
    job_descriptions = relationship("JobDescription", back_populates="company")

class EmployeeProfile(Base, TimestampMixin):
    __tablename__ = "employee_profile"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    job_description_id = Column(Integer, ForeignKey("job_description.id"))
    name = Column(String, nullable=False)
    parsed_content = Column(Text, nullable=False)
    match_percentage = Column(Integer)
    filename = Column(String, nullable=False)

    company = relationship("Company", back_populates="employees")
    job_description = relationship("JobDescription", back_populates="employee_profile") 
    enhanced_profiles = relationship("EnhancedProfile", back_populates="employee")


class JobDescription(Base, TimestampMixin):
    __tablename__ = "job_description"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    filename = Column(String, nullable=False)

    company = relationship("Company", back_populates="job_descriptions")
    employee_profile = relationship("EmployeeProfile", back_populates="job_description")
    enhanced_profiles = relationship("EnhancedProfile", back_populates="job_description", cascade="all, delete-orphan")


class EnhancedProfile(Base, TimestampMixin):
    __tablename__ = "enhanced_profile"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee_profile.id"))
    job_description_id = Column(Integer, ForeignKey("job_description.id"))
    enhanced_content = Column(Text, nullable=False)
    match_percentage = Column(Integer)

    employee = relationship("EmployeeProfile", back_populates="enhanced_profiles")
    job_description = relationship("JobDescription", back_populates="enhanced_profiles")