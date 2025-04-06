from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.dance_class import DanceClass

class ScheduleBase(BaseModel):
    class_id: int
    start_time: datetime
    end_time: datetime
    day_of_week: str
    max_capacity: int
    current_enrolled: Optional[int] = 0

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    day_of_week: Optional[str] = None
    max_capacity: Optional[int] = None

class ScheduleInDB(ScheduleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Schedule(ScheduleInDB):
    dance_class: Optional[DanceClass] = None 