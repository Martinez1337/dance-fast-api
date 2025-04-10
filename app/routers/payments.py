from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

import uuid

from app.schemas.payment import PaymentBaseInfoWithType

from app.schemas.paymentType import PaymentTypeInfo

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
    responses={404: {"description": "Платеж не найден"}}
    # dependencies=[Depends(get_current_active_user)]
)


@router.post("/", response_model=schemas.PaymentBaseInfo, status_code=status.HTTP_201_CREATED)
def create_payment(
        payment_data: schemas.PaymentBase,
        db: Session = Depends(get_db)
):
    payment_type_id = db.query(models.PaymentType).filter(models.PaymentType.id == payment_data.payment_type_id).first()
    if not payment_type_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Тип платежа с идентификатором {payment_data.payment_type_id} не найден",
        )

    payment = models.Payment(
        payment_type_id=payment_data.payment_type_id,
        details=payment_data.details,
        created_at=datetime.now(timezone.utc),
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


@router.get("/", response_model=List[schemas.PaymentBaseInfo])
def get_all_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    payments = db.query(models.Payment).offset(skip).limit(limit).all()
    return payments


@router.get("/withType", response_model=List[schemas.PaymentBaseInfoWithType])
def get_all_payments_with_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    payments = db.query(models.Payment).offset(skip).limit(limit).all()

    payments_with_types = []

    for payment in payments:
        payment_type = db.query(models.PaymentType).filter(models.PaymentType.id == payment.payment_type_id).first()

        payment_with_type = PaymentBaseInfoWithType(
            id=payment.id,
            payment_type_id=payment.payment_type_id,
            details=payment.details,
            payment_type=PaymentTypeInfo(
                id=payment_type.id,
                name=payment_type.name,
            )
        )

        payments_with_types.append(payment_with_type)

    return payments_with_types


@router.get("/{payment_id}", response_model=schemas.PaymentBaseInfo)
def get_payment_by_id(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Платеж не найден"
        )
    return payment


@router.get("/withType/{payment_id}", response_model=schemas.PaymentBaseInfoWithType)
def get_payment_with_type_by_id(payment_id: uuid.UUID, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Платеж не найден"
        )

    payment_type = db.query(models.PaymentType).filter(models.PaymentType.id == payment.payment_type_id).first()
    if payment_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип платежа не найден"
        )

    return PaymentBaseInfoWithType(
        id=payment.id,
        payment_type_id=payment.payment_type_id,
        details=payment.details,
        payment_type=PaymentTypeInfo(
            id=payment_type.id,
            name=payment_type.name
        )
    )
