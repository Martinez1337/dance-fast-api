from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.instructor import Instructor

class DanceClassBase(BaseModel):
    name: str
    description: Optional[str] = None
    instructor_id: int
    level: str
    style: str
    duration_minutes: int
    price: float
    image_url: Optional[str] = None

class DanceClassCreate(DanceClassBase):
    pass

class DanceClassUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    instructor_id: Optional[int] = None
    level: Optional[str] = None
    style: Optional[str] = None
    duration_minutes: Optional[int] = None
    price: Optional[float] = None
    image_url: Optional[str] = None

class DanceClassInDB(DanceClassBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DanceClass(DanceClassInDB):
    instructor: Optional[Instructor] = None 