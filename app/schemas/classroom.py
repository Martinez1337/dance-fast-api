from pydantic import BaseModel
import uuid


class ClassroomBase(BaseModel):
    """Базовая схема зала."""
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class ClassroomInfo(ClassroomBase):
    id: uuid.UUID
    terminated: bool

    class Config:
        from_attributes = True
