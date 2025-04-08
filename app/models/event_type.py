from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class EventType(BaseModel):
    __tablename__ = "event_types"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Связи
    events = relationship("Event", back_populates="event_type") 