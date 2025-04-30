from sqlalchemy.orm import Session
from app.database.dbSession import safe_commit_transaction
from app.database import models, dto
from fastapi import UploadFile
from app.exception_handlers import ResourceNotFoundException, BadRequestException
from app.utils.logger import get_logger
from app.utils.helpers import extract_text_from_file
from app.services.match import calculate_similarity
from app.services.enhance import enhance_profile
from app.services.enhance import enhance_profile_with_prompt

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

def createEmployeeProfile(db: Session, profile: dto.EmployeeProfileCreate):
    company = db.query(models.Company).filter(models.Company.id == profile.company_id).first()
    if not company:
        raise BadRequestException(f"Company with ID {profile.company_id} does not exist.")
    
    jd = db.query(models.JobDescription).filter(models.JobDescription.id == profile.jd_id).first()
    if not jd:
        raise BadRequestException(f"Job description with ID {profile.jd_id} does not exist.")
    
    # Calculate match percentage
    match_percentage = calculate_similarity(jd.content, profile.parsed_content)

    new_profile = models.EmployeeProfile(
        company_id=profile.company_id,
        job_description_id=profile.jd_id,
        filename=profile.filename,
        match_percentage=match_percentage,
        name=profile.name,
        parsed_content= profile.parsed_content
    )
  
    db.add(new_profile)
    with safe_commit_transaction(db):
        pass
    db.refresh(new_profile)

    log.info(f"Employee profile created with ID: {new_profile.id} and match percentage: {match_percentage}")
    return {
        "profile_id": new_profile.id,
        "name": new_profile.name,
        "match_percentage": match_percentage,
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

def createFileEntry(db: Session, file: UploadFile, file_type: str, company_id: int, name: str, jd_id: int):
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
        profile = dto.EmployeeProfileCreate(company_id=company_id, name=name, filename=file.filename, parsed_content=parsed_content, jd_id=jd_id)
        if not jd_id:
            log.error("JD ID is required for profile creation.")
            raise BadRequestException("JD ID is required for profile creation.")
        return createEmployeeProfile(db, profile)
    

def enhanceProfile(db: Session, profile_id: int, jd_id: int):
    # if already enhanced, return the existing profile
    existing_enhanced_profile = db.query(models.EnhancedProfile).filter(
        models.EnhancedProfile.employee_id == profile_id,
        models.EnhancedProfile.job_description_id == jd_id
    ).first()

    if existing_enhanced_profile:
        return {
            "message": "Profile already enhanced",
            "match_percentage": existing_enhanced_profile.match_percentage,
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

    enhanced_content = enhance_profile(profile.parsed_content, jd.content)

     # Calculate match percentage
    match_percentage = calculate_similarity(jd.content, enhanced_content)

    enhanced_profile = models.EnhancedProfile(
        employee_id=profile.id,
        job_description_id=jd.id,
        match_percentage=match_percentage,
        enhanced_content=enhanced_content
    )
    db.add(enhanced_profile)

    with safe_commit_transaction(db):
        pass
    db.refresh(enhanced_profile)
    return {
        "message": "Profile enhanced successfully",
        "enhanced_content": enhanced_content
    }

def enhanceProfileWithPrompt(db: Session, profile_id: int, jd_id: int, prompt: str):
    # if already enhanced, return the existing profile
    existing_enhanced_profile = db.query(models.EnhancedProfile).filter(
        models.EnhancedProfile.employee_id == profile_id,
        models.EnhancedProfile.job_description_id == jd_id
    ).first()

    jd = db.query(models.JobDescription).filter(models.JobDescription.id == jd_id).first()

    if not jd:
        log.error(f"Job description with ID {jd_id} does not exist.")
        raise ResourceNotFoundException(f"Job description with ID {jd_id} does not exist.")
    
    if not existing_enhanced_profile:
        log.error(f"Enhanced profile with ID {profile_id} does not exist.")
        raise ResourceNotFoundException(f"Enhanced profile with ID {profile_id} does not exist.")

    enhanced_content = enhance_profile_with_prompt(existing_enhanced_profile.enhanced_content, jd.content, prompt)

    # Calculate match percentage
    match_percentage = calculate_similarity(jd.content, enhanced_content)

    existing_enhanced_profile.enhanced_content = enhanced_content
    existing_enhanced_profile.match_percentage = match_percentage
    db.add(existing_enhanced_profile)
    with safe_commit_transaction(db):
        pass
    db.refresh(existing_enhanced_profile)
    return {
        "message": "Profile enhanced successfully with the given prompt",
        "match_percentage": match_percentage,
        "enhanced_content": enhanced_content
    }