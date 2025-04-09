from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
import uuid

class AdminBase(BaseModel):
    """Базовая схема администратора."""
    user_id: uuid.UUID