import uuid
from pydantic import BaseModel
from app.schemas.user import UserBase, UserCreate
from app.schemas.level import LevelBaseInfo
from typing import List


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


class StudentGroupInfo(StudentBaseInfo):
    user: UserBase
    level: LevelBaseInfo

    class Config:
        from_attributes = True


class StudentFullInfo(StudentBaseInfo):
    user: UserBase
    level: LevelBaseInfo
    groups: "List[MemberGroupBase]"

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


from app.schemas.association import MemberGroupBase

StudentFullInfo.model_rebuild()
