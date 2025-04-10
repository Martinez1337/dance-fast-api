from pydantic import BaseModel
from app.schemas.user import UserBase
import uuid


class StudentBase(BaseModel):
    """Базовая схема студента."""
    user_id: uuid.UUID
    level_id: uuid.UUID

    class Config:
        from_attributes = True


class StudentBaseInfo(StudentBase):
    id: uuid.UUID
    terminated: bool

    class Config:
        from_attributes = True


class StudentResponse(UserBase):
    level_name: str

    class Config:
        from_attributes = True
