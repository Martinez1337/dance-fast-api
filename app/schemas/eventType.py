from pydantic import BaseModel
import uuid


class EventTypeBase(BaseModel):
    """Базовая схема типа мероприятия."""
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class EventTypeInfo(EventTypeBase):
    id: uuid.UUID
    terminated: bool

    class Config:
        from_attributes = True
