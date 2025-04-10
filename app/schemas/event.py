from pydantic import BaseModel
from datetime import datetime
import uuid

from app.schemas.eventType import EventTypeInfo


class EventBase(BaseModel):
    """Базовая схема мероприятия."""
    event_type_id: uuid.UUID
    name: str
    description: str | None = None
    start_time: datetime
    photo_url: str


class EventBaseInfo(EventBase):
    id: uuid.UUID


class EventBaseInfoWithType(EventBaseInfo):
    event_type: EventTypeInfo
