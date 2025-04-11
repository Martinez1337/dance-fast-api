from pydantic import BaseModel
from app.schemas.user import UserBase, UserCreate
from app.schemas.level import LevelBaseInfo
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


class StudentFullInfo(StudentBaseInfo):
    user: UserBase
    level: LevelBaseInfo

    class Config:
        from_attributes = True


class StudentCreate(UserCreate):
    level_id: uuid.UUID

    class Config:
        from_attributes = True


class StudentResponse(UserBase):
    level_name: str

    class Config:
        from_attributes = True
