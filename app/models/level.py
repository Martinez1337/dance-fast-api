from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Level(BaseModel):
    __tablename__ = "levels"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Связи
    students = relationship("Student", back_populates="level")
    groups = relationship("Group", back_populates="level") 