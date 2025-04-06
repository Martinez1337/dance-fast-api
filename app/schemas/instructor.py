from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InstructorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    specialization: Optional[str] = None
    photo_url: Optional[str] = None

class InstructorCreate(InstructorBase):
    pass

class InstructorUpdate(InstructorBase):
    name: Optional[str] = None
    is_active: Optional[bool] = None

class InstructorInDB(InstructorBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Instructor(InstructorInDB):
    pass 