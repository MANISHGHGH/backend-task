from pydantic import BaseModel
from typing import List, Optional

class TeamMember(BaseModel):
    id: int
    name: str
    role: str

class ProjectDetails(BaseModel):
    start_date: str
    end_date: str
    team_members: List[TeamMember]

class Project(BaseModel):
    project_id: int
    name: str
    details: ProjectDetails

class Contact(BaseModel):
    email: str
    phone: str

class Employee(BaseModel):
    id: int
    name: str
    contact: Contact
    projects: List[Project]

class UpdateUser(BaseModel):
    name: Optional[str] = None
    contact: Optional[Contact] = None
    projects: Optional[List[Project]] = None
