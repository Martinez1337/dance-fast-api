from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from app.database import get_db
from app import models, schemas
from app.auth.jwt import get_current_active_user, get_current_admin
from app.auth.password import get_password_hash

import uuid

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
    responses={404: {"description": "Подписка не найдена"}}
)

@router.post("/", response_model=schemas.SubscriptionInfo, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription_data: schemas.SubscriptionBase,
    db: Session = Depends(get_db)
):
    # Создаем подписку
    subscription = models.Subscription(
        student_id=subscription_data.student_id,
        subscription_template_id=subscription_data.subscription_template_id,
        expiration_date=subscription_data.expiration_date,
        payment_id=subscription_data.payment_id,
        created_at=datetime.now(timezone.utc)
    )

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription

@router.get("/", response_model=List[schemas.SubscriptionInfo])
async def get_all_subscriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subscriptions = db.query(models.Subscription).offset(skip).limit(limit).all()
    return subscriptions

@router.get("/{subscription_id}", response_model=schemas.SubscriptionInfo)
async def get_subscription_by_id(subscription_id: uuid.UUID, db: Session = Depends(get_db)):
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Подписка не найдена"
        )
    return db_subscription 