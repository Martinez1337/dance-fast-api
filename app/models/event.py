from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Event(BaseModel):
    __tablename__ = "events"

    event_type_id = Column(UUID(as_uuid=True), ForeignKey("event_types.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    photo_url = Column(String, nullable=False)

    # Связи
    event_type = relationship("EventType", back_populates="events") 