from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.auth.jwt import get_current_active_user, get_current_admin
from app.auth.password import get_password_hash

router = APIRouter(
    prefix="/subscription_templates",
    tags=["subscription_templates"],
    responses={404: {"description": "Шаблон подписки не найден"}}
)

@router.post("/", response_model=schemas.SubscriptionTemplateBase, status_code=status.HTTP_201_CREATED)
async def create_subscription_template(
    subscription_template_data: schemas.SubscriptionTemplateCreate,
    db: Session = Depends(get_db)
):
    # Проверяем, существует ли пользователь с таким email
    db_subscription_template = db.query(models.SubscriptionTemplate).filter(models.SubscriptionTemplate.name == subscription_template_data.name).first()
    if db_subscription_template:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Шаблон подписки уже существует",
        )
    
    # Создаем пользователя
    subscription_template = models.SubscriptionTemplate(
        name=subscription_template_data.name,
        description=subscription_template_data.description,
        price=subscription_template_data.price,
        duration=subscription_template_data.duration,
        is_active=subscription_template_data.is_active,
        created_at=datetime.now(timezone.utc)
    )

    db.add(subscription_template)
    db.commit()
    db.refresh(subscription_template)

    return subscription_template

@router.get("/", response_model=List[schemas.SubscriptionTemplateBase])
async def get_all_subscription_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subscription_templates = db.query(models.SubscriptionTemplate).offset(skip).limit(limit).all()
    return subscription_templates

@router.get("/{subscription_template_id}", response_model=schemas.SubscriptionTemplateBase)
async def get_subscription_template_by_id(subscription_template_id: int, db: Session = Depends(get_db)):
    db_subscription_template = db.query(models.SubscriptionTemplate).filter(models.SubscriptionTemplate.id == subscription_template_id).first()
    if db_subscription_template is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Шаблон подписки не найден"
        )
    return db_subscription_template 