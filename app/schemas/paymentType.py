from pydantic import BaseModel
import uuid


class PaymentTypeBase(BaseModel):
    """Базовая схема типа платежа."""
    name: str

    class Config:
        from_attributes = True


class PaymentTypeInfo(PaymentTypeBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
