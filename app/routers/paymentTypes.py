from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

import uuid

router = APIRouter(
    prefix="/paymentTypes",
    tags=["payment types"],
    responses={404: {"description": "Тип платежа не найден"}}
    # dependencies=[Depends(get_current_active_user)]
)


@router.post("/", response_model=schemas.PaymentTypeInfo, status_code=status.HTTP_201_CREATED)
def create_payment_type(
        payment_type_data: schemas.PaymentTypeBase,
        db: Session = Depends(get_db)
):
    payment_type = models.PaymentType(
        name=payment_type_data.name,
    )

    db.add(payment_type)
    db.commit()
    db.refresh(payment_type)

    return payment_type


@router.get("/", response_model=List[schemas.PaymentTypeInfo])
def get_all_payment_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    payment_types = db.query(models.PaymentType).offset(skip).limit(limit).all()
    return payment_types


@router.get("/{payment_type_id}", response_model=schemas.PaymentTypeInfo)
def get_payment_type_by_id(payment_type_id: uuid.UUID, db: Session = Depends(get_db)):
    payment_type = db.query(models.PaymentType).filter(models.PaymentType.id == payment_type_id).first()
    if payment_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип платежа не найден"
        )
    return payment_type
