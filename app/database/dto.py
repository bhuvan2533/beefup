from pydantic import BaseModel
from typing import Optional, List

class CompanyCreate(BaseModel):
    name: str

class EmployeeProfileCreate(BaseModel):
    company_id: int
    name: str
    parsed_content: str

class JobDescriptionCreate(BaseModel):
    company_id: int
    jd_text: str