from sqlalchemy.orm import Session
from app.database.dbSession import safe_commit_transaction
from app.database import models, dto
from fastapi import UploadFile
from app.exception_handlers import ResourceNotFoundException, BadRequestException
from app.utils.logger import get_logger
from app.utils.helpers import extract_text_from_file
from app.services.enhance import enhanceProfileWithJd, extractFromProfile
from app.database.dto import ProfileUpdateRequest
log = get_logger()

def createCompany(db: Session, company: dto.CompanyCreate):
    new_company = models.Company(name=company.name)
    db.add(new_company)
    with safe_commit_transaction(db):
        pass
    return {
        "id": new_company.id,
        "name": new_company.name,
    }

def getCompanyByName(db: Session, name: str):
    company = db.query(models.Company).filter(
        models.Company.name == name
    ).first()
    if not company:
        raise ResourceNotFoundException(f"Company with name {name} does not exist.")
    return {
        "id": company.id,
        "name": company.name,
    }

async def createEmployeeProfile(db: Session, profile: dto.EmployeeProfileCreate):
    company = db.query(models.Company).filter(models.Company.id == profile.company_id).first()
    if not company:
        raise BadRequestException(f"Company with ID {profile.company_id} does not exist.")
    
    jd = db.query(models.JobDescription).filter(models.JobDescription.id == profile.jd_id).first()
    if not jd:
        raise BadRequestException(f"Job description with ID {profile.jd_id} does not exist.")

    extracted_content = await extractFromProfile(profile.parsed_content)

    if not extracted_content:
        log.error(f"Profile content is empty or could not be parsed: {profile.filename}")
        raise BadRequestException("Profile content is empty or could not be parsed.")
    
    
    new_profile = models.EmployeeProfile(
        company_id=profile.company_id,
        job_description_id=profile.jd_id,
        filename=profile.filename,
        name=profile.name,
        parsed_content= extracted_content
    )
  
    db.add(new_profile)
    with safe_commit_transaction(db):
        pass
    db.refresh(new_profile)

    log.info(f"Employee profile created with ID: {new_profile.id}")
    return {
        "profile_id": new_profile.id,
        "name": new_profile.name,
        "message": "Employee profile created successfully",
    }

def createJobDescription(db: Session, jd: dto.JobDescriptionCreate):
    company = db.query(models.Company).filter(models.Company.id == jd.company_id).first()
    if not company:
        raise BadRequestException(f"Company with ID {jd.company_id} does not exist.")
    
    new_jd = models.JobDescription(
        company_id=jd.company_id,
        content=jd.parsed_content,
        title=jd.title,
        filename=jd.filename
    )

    db.add(new_jd)
    with safe_commit_transaction(db): 
        pass
    db.refresh(new_jd)
    log.info(f"Job description created with ID: {new_jd.id} for company ID: {jd.company_id}")
    return {
        "jd_id": new_jd.id,
        "message": "Job description created successfully",
    }

async def createFileEntry(db: Session, file: UploadFile, file_type: str, company_id: int, name: str, jd_id: int):
    if file_type not in ["jd", "profile"]:
        log.error(f"Invalid file type: {file_type}")
        raise ResourceNotFoundException("Invalid file type. Supported types are 'jd' and 'profile'.")
    parsed_content = extract_text_from_file(file)

    if not parsed_content:
        log.error(f"File is empty or could not be parsed: {file.filename}")
        raise BadRequestException("File is empty or could not be parsed.")
    
    if file_type == "jd": 
        jd = dto.JobDescriptionCreate(company_id=company_id, filename=file.filename, title=name, parsed_content=parsed_content)
        return createJobDescription(db, jd)
    elif file_type == "profile":
        if not jd_id:
            log.error("JD ID is required for profile creation.")
            raise BadRequestException("JD ID is required for profile creation.")
        profile = dto.EmployeeProfileCreate(company_id=company_id, name=name, filename=file.filename, parsed_content=parsed_content, jd_id=jd_id)
        return await createEmployeeProfile(db, profile)
    

async def enhanceProfile(db: Session, profile_id: int, jd_id: int):
    # if already enhanced, return the existing profile
    existing_enhanced_profile = db.query(models.EnhancedProfile).filter(
        models.EnhancedProfile.employee_id == profile_id,
        models.EnhancedProfile.job_description_id == jd_id
    ).first()

    if existing_enhanced_profile:
        return {
            "message": "Profile already enhanced",
            "enhanced_content": existing_enhanced_profile.enhanced_content
        }

    profile = db.query(models.EmployeeProfile).filter(models.EmployeeProfile.id == profile_id).first()
    if not profile:
        log.error(f"Employee profile with ID {profile_id} does not exist.")
        raise ResourceNotFoundException(f"Employee profile with ID {profile_id} does not exist.")
    
    jd = db.query(models.JobDescription).filter(models.JobDescription.id == jd_id).first()
    if not jd:
        log.error(f"Job description with ID {jd_id} does not exist.")
        raise ResourceNotFoundException(f"Job description with ID {jd_id} does not exist.")

    enhanced_content = await enhanceProfileWithJd(jd_content=jd.content, structured_profile=profile.parsed_content)

    enhanced_profile = models.EnhancedProfile(
        employee_id=profile.id,
        job_description_id=jd.id,
        enhanced_content=enhanced_content
    )
    db.add(enhanced_profile)

    with safe_commit_transaction(db):
        pass
    db.refresh(enhanced_profile)
    return {
        "enhanced_profile_id": enhanced_profile.id,
        "message": "Profile enhanced successfully",
        "enhanced_content": enhanced_content
    }

def updateProfile(db: Session, request: ProfileUpdateRequest):
    existing_enhanced_profile = db.query(models.EnhancedProfile).filter(
        models.EnhancedProfile.id == request.enhanced_profile_id
    ).first()

    if not existing_enhanced_profile:
        log.error(f"Enhanced profile with ID {request.enhanced_profile_id} does not exist.")
        raise ResourceNotFoundException(f"Enhanced profile with ID {request.enhanced_profile_id} does not exist.")

    existing_enhanced_profile.enhanced_content = request.content
    with safe_commit_transaction(db):
        pass
    db.refresh(existing_enhanced_profile)
    return {
        "message": "Profile updated successfully",
        "profile": existing_enhanced_profile.enhanced_content
    }

def getEnhancedProfile(db: Session, enhanced_profile_id: int):
    enhanced_profile = db.query(models.EnhancedProfile).filter(
        models.EnhancedProfile.id == enhanced_profile_id
    ).first()

    if not enhanced_profile:
        log.error(f"Enhanced profile with ID {enhanced_profile_id} does not exist.")
        raise ResourceNotFoundException(f"Enhanced profile with ID {enhanced_profile_id} does not exist.")

    return {
        "message": "Enhanced profile retrieved successfully",
        "employee_id": enhanced_profile.employee_id,
        "job_description_id": enhanced_profile.job_description_id,
        "enhanced_profile_id": enhanced_profile.id,
        "enhanced_content": enhanced_profile.enhanced_content
    }