from typing import List, Optional
from pydantic import BaseModel

class Project(BaseModel):
    title: Optional[str] = None
    tech_stack: Optional[List[str]] = []
    description: Optional[str] = None
    contribution: Optional[List[str]] = []

    class Config:
        orm_mode = True


class Technologies(BaseModel):
    backend: Optional[List[str]] = []
    frontend: Optional[List[str]] = []
    database: Optional[List[str]] = []
    tools: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    AI_technologies: Optional[List[str]] = []

    class Config:
        orm_mode = True


class EnhancedProfile(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    summary: Optional[str] = None
    technologies: Optional[Technologies] = Technologies()
    skills: Optional[List[str]] = []
    enhanced_projects: Optional[List[Project]] = []
    skill_gaps: Optional[List[str]] = []

    class Config:
        orm_mode = True