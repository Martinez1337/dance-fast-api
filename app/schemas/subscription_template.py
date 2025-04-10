from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
import decimal

class SubscriptionTemplateBase(BaseModel):
    """Базовая схема шаблона подписки."""
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    lessons_count: int
    expiration_date: datetime
    expiration_day_count: int
    price: decimal.Decimal


class UserBaseInfo(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    description: Optional[str] = None
    phone_number: str
    role: str

class SubscriptionTemplateCreate(BaseModel):
    """Схема для создания пользователя."""
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    description: Optional[str] = None
    phone_number: str
    password: str

