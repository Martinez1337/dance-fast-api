from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    