from pydantic import BaseModel
import uuid
from datetime import time

class SlotBase(BaseModel):
    """Базовая схема слота."""
    teacher_id: uuid.UUID
    day_of_week: int
    start_time: time
    end_time: time

    class Config:
        from_attributes = True


class SlotBaseInfo(SlotBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
