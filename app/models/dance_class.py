from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class DanceClass(Base):
    __tablename__ = "dance_classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    instructor_id = Column(Integer, ForeignKey("instructors.id"))
    level = Column(String)  # beginner, intermediate, advanced
    style = Column(String, index=True)  # salsa, bachata, hip-hop, etc.
    duration_minutes = Column(Integer)
    price = Column(Float)
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    instructor = relationship("Instructor") 