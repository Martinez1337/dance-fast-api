from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
import decimal


class SubscriptionTemplateBase(BaseModel):
    """Базовая схема шаблона подписки."""
    name: str
    description: Optional[str] = None
    lesson_count: int
    expiration_date: datetime
    expiration_day_count: int
    price: decimal.Decimal
    active: bool

    class Config:
        from_attributes = True


class SubscriptionTemplateInfo(SubscriptionTemplateBase):
    id: uuid.UUID

    class Config:
        from_attributes = True

