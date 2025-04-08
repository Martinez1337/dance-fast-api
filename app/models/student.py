from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    middle_name = Column(String, nullable=True)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    level = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    level_id = Column(UUID(as_uuid=True), ForeignKey("levels.id"), nullable=False)

    user = relationship("User", back_populates="student")
    level = relationship("Level", back_populates="students")
    groups = relationship("StudentGroup", back_populates="student")
    subscriptions = relationship("Subscription", back_populates="student")
    