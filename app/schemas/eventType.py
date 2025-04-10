from pydantic import BaseModel
import uuid


class EventTypeBase(BaseModel):
    """Базовая схема типа мероприятия."""
    name: str
    description: str | None = None


class EventTypeInfo(EventTypeBase):
    id: uuid.UUID
    terminated: bool
