from pydantic import BaseModel
from app.schemas.level import LevelInfo
from app.schemas.association import GroupTeacherBase, GroupStudentBase
import uuid
from typing import Optional, List
from datetime import datetime


class GroupBase(BaseModel):
    """Базовая схема группы."""
    name: str
    description: Optional[str] = None
    level_id: uuid.UUID
    max_capacity: int

    class Config:
        from_attributes = True


class GroupBaseInfo(GroupBase): 
    id: uuid.UUID
    terminated: bool

    class Config:
        from_attributes = True


class GroupFullInfo(GroupBaseInfo):
    level: LevelInfo
    students: List[GroupStudentBase]
    teachers: List[GroupTeacherBase]

    class Config:
        from_attributes = True
