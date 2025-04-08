from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Classroom(BaseModel):
    __tablename__ = "classrooms"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Связи
    lessons = relationship("Lesson", back_populates="classroom") 