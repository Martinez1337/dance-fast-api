from pydantic import BaseModel
from datetime import datetime
import uuid

class EventBase(BaseModel):
    """Базовая схема мероприятия."""
    event_type_id: uuid.UUID
    name: str
    description: str | None = None
    start_time: datetime
    photo_url: str

class EventBaseInfo(BaseModel):
    id: uuid.UUID
    event_type_id: uuid.UUID
    name: str
    description: str | None = None
    start_time: datetime
    photo_url: str