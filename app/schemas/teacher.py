from pydantic import BaseModel
from app.schemas.user import UserBase
import uuid


class TeacherBase(BaseModel):
    """Базовая схема преподавателя."""
    user_id: uuid.UUID

    class Config:
        from_attributes = True


class TeacherBaseInfo(TeacherBase):
    id: uuid.UUID
    terminated: bool

    class Config:
        from_attributes = True


class TeacherFullInfo(TeacherBaseInfo):
    user: UserBase

    class Config:
        from_attributes = True
