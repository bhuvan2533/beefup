from pydantic import BaseModel
from typing import Optional

class CompanyCreate(BaseModel):
    name: str

class EmployeeProfileCreate(BaseModel):
    company_id: int
    name: str
    parsed_content: str
    filename: Optional[str] = None
    jd_id: int

class JobDescriptionCreate(BaseModel):
    company_id: int
    parsed_content: str
    title: Optional[str] = None
    filename: Optional[str] = None