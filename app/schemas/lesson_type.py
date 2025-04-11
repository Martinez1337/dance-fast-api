from pydantic import BaseModel
import uuid


class LessonTypeBase(BaseModel):
    """Базовая схема типа платежа."""
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class LessonTypeInfo(LessonTypeBase):
    id: uuid.UUID
    terminated: bool

    class Config:
        from_attributes = True
