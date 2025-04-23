# app/database/crud.py
from sqlalchemy.orm import Session
from app.database import models, dto

def create_company(db: Session, company: dto.CompanyCreate):
    new_company = models.Company(name=company.name)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

def create_employee_profile(db: Session, profile: dto.EmployeeProfileCreate):
    new_profile = models.EmployeeProfile(
        company_id=profile.company_id,
        name=profile.name,
        parsed_content=profile.parsed_content
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

def create_job_description(db: Session, jd: dto.JobDescriptionCreate):
    new_jd = models.JobDescription(
        company_id=jd.company_id,
        jd_text=jd.jd_text
    )
    db.add(new_jd)
    db.commit()
    db.refresh(new_jd)
    return new_jd
