from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.user import User
from app.schemas.schedule import Schedule

class BookingBase(BaseModel):
    user_id: int
    schedule_id: int
    status: str
    is_paid: bool = False

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    status: Optional[str] = None
    is_paid: Optional[bool] = None

class BookingInDB(BookingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Booking(BookingInDB):
    user: Optional[User] = None
    schedule: Optional[Schedule] = None 