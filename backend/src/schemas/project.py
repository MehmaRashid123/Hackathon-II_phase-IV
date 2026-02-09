from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    workspace_id: UUID # Client should provide which workspace to create project in

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectRead(ProjectBase):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
