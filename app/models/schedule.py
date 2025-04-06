from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("dance_classes.id"))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    day_of_week = Column(String)  # Monday, Tuesday, etc.
    max_capacity = Column(Integer)
    current_enrolled = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    dance_class = relationship("DanceClass") 