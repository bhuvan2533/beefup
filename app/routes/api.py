from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import crud, dto
from app.database.dbSession import get_db
from typing import Optional
from app.database.dto import ProfileUpdateRequest

router = APIRouter()

@router.post("/company")
def create_company(company: dto.CompanyCreate, db: Session = Depends(get_db)):
    return crud.createCompany(db, company)

# Temporary API for internal usage
@router.get("/company/{name}")
def get_company_by_name(name: str, db: Session = Depends(get_db)):
    return crud.getCompanyByName(db, name)

@router.post("/upload/{file_type}")
async def upload_file(
    file_type: str,  # "jd" or "profile"
    file: UploadFile = File(...),
    company_id: int = Form(...), 
    jd_id: Optional[str] = Form(None),
    name: str = Form(...), # for profile -> name of employee / for jd -> title of jd
    db: Session = Depends(get_db)):
    jd_id_int = int(jd_id) if jd_id and jd_id.strip().isdigit() else None
    return await crud.createFileEntry(db, file, file_type, company_id, name, jd_id=jd_id_int)

@router.post("/enhance-profile")
async def enhance_profile(
    jd_id: int,
    profile_id: int,
    db: Session = Depends(get_db)):
    return await crud.enhanceProfile(db, profile_id, jd_id)

@router.put("/update-profile")
async def update_profile(
    request: ProfileUpdateRequest,
    db: Session = Depends(get_db)):
    return crud.updateProfile(db, request)


@router.get("/profile/{enhanced_profile_id}")
async def get_enhanced_profile(
    enhanced_profile_id: int,
    db: Session = Depends(get_db)):
    return crud.getEnhancedProfile(db, enhanced_profile_id)