from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
import uuid

class UserBase(BaseModel):
    """Базовая схема пользователя."""
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    description: Optional[str] = None
    phone_number: str

class UserCreate(UserBase):
    """Схема для создания пользователя."""
    password: str
    level_id: uuid.UUID

    @validator('password')
    def password_strength(cls, v):
        """Проверяет сложность пароля."""
        if len(v) < 8:
            raise ValueError('Пароль должен содержать минимум 8 символов')
        return v

class UserLogin(BaseModel):
    """Схема для входа пользователя."""
    email: EmailStr
    password: str    


class UserResponse(UserBase):
    """Схема для ответа с данными пользователя."""
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    role: str
    level_name: str

    class Config:
        from_attributes = True 