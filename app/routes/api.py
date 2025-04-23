from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import crud, dto
from app.database.dbSession import get_db

router = APIRouter()

@router.post("/company/")
def create_company(company: dto.CompanyCreate, db: Session = Depends(get_db)):
    return crud.create_company(db, company)

@router.post("/employee/")
def create_employee(profile: dto.EmployeeProfileCreate, db: Session = Depends(get_db)):
    return crud.create_employee_profile(db, profile)

@router.post("/upload-jd/")
def upload_jd(jd: dto.JobDescriptionCreate, db: Session = Depends(get_db)):
    return crud.create_job_description(db, jd)
