from pydantic import BaseModel
from app.schemas.level import LevelBaseInfo
from app.schemas.association import StudentGroupBase, TeacherGroupBase
import uuid
from typing import Optional, List


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
    level: LevelBaseInfo
    students: List[StudentGroupBase]
    teachers: List[TeacherGroupBase]

    class Config:
        from_attributes = True
