from sqlalchemy.orm import Session
from app.database.dbSession import safe_commit_transaction
from app.database import models, dto
from app.exception_handlers import NotFoundException

def createCompany(db: Session, company: dto.CompanyCreate):
    new_company = models.Company(name=company.name)
    db.add(new_company)
    safe_commit_transaction(db)
    return {
        "id": new_company.id,
        "name": new_company.name,
    }

def createEmployeeProfile(db: Session, profile: dto.EmployeeProfileCreate):
    company = db.query(models.Company).filter(models.Company.id == profile.company_id).first()
    if not company:
         NotFoundException(f"Company with id {profile.company_id} does not exist.")
    
    new_profile = models.EmployeeProfile(
        company_id=profile.company_id,
        name=profile.name,
        parsed_content=profile.parsed_content
    )
  
    db.add(new_profile)
    safe_commit_transaction(db)
    return {
        "id": new_profile.id,
        "company_id": new_profile.company_id,
        "name": new_profile.name,
    }

def createJobDescription(db: Session, jd: dto.JobDescriptionCreate):
    new_jd = models.JobDescription(
        company_id=jd.company_id,
        jd_text=jd.jd_text
    )
    db.add(new_jd)
    safe_commit_transaction(db)
    return {
        "id": new_jd.id,
        "company_id": new_jd.company_id,
    }
