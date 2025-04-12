from pydantic import BaseModel
from app.schemas.user import UserBase
import uuid


class AdminBase(BaseModel):
    """Базовая схема администратора."""
    user_id: uuid.UUID

    class Config:
        from_attributes = True


class AdminBaseInfo(AdminBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class AdminFullInfo(AdminBaseInfo):
    user: UserBase

    class Config:
        from_attributes = True
