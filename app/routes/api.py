from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import crud, dto
from app.database.dbSession import get_db
from typing import Optional

router = APIRouter()

@router.post("/company/")
def create_company(company: dto.CompanyCreate, db: Session = Depends(get_db)):
    return crud.createCompany(db, company)

@router.post("/upload/{file_type}")
async def upload_file(
    file_type: str,  # "jd" or "profile"
    file: UploadFile = File(...),
    company_id: int = Form(...), 
    jd_id: Optional[str] = Form(None),
    name: str = Form(...), # for profile -> name of employee / for jd -> title of jd
    db: Session = Depends(get_db)):
    jd_id_int = int(jd_id) if jd_id and jd_id.strip().isdigit() else None
    return crud.createFileEntry(db, file, file_type, company_id, name, jd_id=jd_id_int)


@router.post("/enhance-profile/")
async def enhance_profile(
    jd_id: int,
    profile_id: int,
    db: Session = Depends(get_db)):
    return crud.enhanceProfile(db, profile_id, jd_id)

@router.get("/enhance-with-prompt/")
async def enhance_with_prompt(
    jd_id: int,
    profile_id: int,
    prompt: str,
    db: Session = Depends(get_db)):
    return crud.enhanceProfileWithPrompt(db, profile_id, jd_id, prompt)