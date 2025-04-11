import uuid
from typing import List
from pydantic import BaseModel
from app.schemas.user import UserBase
from app.schemas.association import MemberGroupBase


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


class TeacherGroupInfo(TeacherBaseInfo):
    user: UserBase

    class Config:
        from_attributes = True


class TeacherFullInfo(TeacherBaseInfo):
    user: UserBase
    groups: List[MemberGroupBase]

    class Config:
        from_attributes = True
