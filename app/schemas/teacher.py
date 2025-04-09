from pydantic import BaseModel
import uuid

class TeacherBase(BaseModel):
    """Базовая схема преподавателя."""
    user_id: uuid.UUID