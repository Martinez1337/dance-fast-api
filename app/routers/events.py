from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db
from datetime import datetime, timezone

import uuid

from app.schemas.eventType import EventTypeInfo

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Мероприятие не найдено"}}
    # dependencies=[Depends(get_current_active_user)]
)


@router.post("/", response_model=schemas.EventInfo, status_code=status.HTTP_201_CREATED)
async def create_event(
        event_data: schemas.EventBase,
        db: Session = Depends(get_db)
):
    event_type_id = db.query(models.EventType).filter(models.EventType.id == event_data.event_type_id).first()
    if not event_type_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Тип мероприятия с идентификатором {event_data.event_type_id} не найден",
        )

    event = models.Event(
        event_type_id=event_data.event_type_id,
        name=event_data.name,
        description=event_data.description,
        start_time=event_data.start_time,
        photo_url=event_data.photo_url,
        created_at=datetime.now(timezone.utc)
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.get("/", response_model=List[schemas.EventInfo])
async def get_all_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return events


@router.get("/full-info", response_model=List[schemas.EventFullInfo])
async def get_all_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = db.query(models.Event).offset(skip).limit(limit).all()
    return events


@router.get("/{event_id}", response_model=schemas.EventInfo)
async def get_event_by_id(event_id: uuid.UUID, db: Session = Depends(get_db)):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие не найдено"
        )
    return db_event


@router.get("/full-info/{event_id}", response_model=schemas.EventFullInfo)
async def get_event_with_type_by_id(event_id: uuid.UUID, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мероприятие не найдено"
        )

    event_type = db.query(models.EventType).filter(models.EventType.id == event.event_type_id).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тип мероприятия не найден"
        )

    return event
