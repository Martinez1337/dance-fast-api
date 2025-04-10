from pydantic import BaseModel
from app.schemas.paymentType import PaymentTypeInfo
import uuid


class PaymentBase(BaseModel):
    """Базовая схема платежа."""
    payment_type_id: uuid.UUID
    details: str | None = None

    class Config:
        from_attributes = True


class PaymentBaseInfo(PaymentBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class PaymentBaseInfoWithType(PaymentBaseInfo):
    payment_type: PaymentTypeInfo

    class Config:
        from_attributes = True
