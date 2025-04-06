from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
    responses={404: {"description": "Расписание не найдено"}},
)

@router.post("/", response_model=schemas.Schedule, status_code=status.HTTP_201_CREATED)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли класс
    dance_class = db.query(models.DanceClass).filter(models.DanceClass.id == schedule.class_id).first()
    if not dance_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Класс не найден"
        )
    
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.get("/", response_model=List[schemas.Schedule])
def read_schedules(
    skip: int = 0, 
    limit: int = 100, 
    class_id: Optional[int] = None,
    day_of_week: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Schedule)
    
    if class_id:
        query = query.filter(models.Schedule.class_id == class_id)
    if day_of_week:
        query = query.filter(models.Schedule.day_of_week == day_of_week)
    if date_from:
        query = query.filter(models.Schedule.start_time >= date_from)
    if date_to:
        query = query.filter(models.Schedule.start_time <= date_to)
    
    schedules = query.offset(skip).limit(limit).all()
    return schedules

@router.get("/{schedule_id}", response_model=schemas.Schedule)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Расписание не найдено"
        )
    return db_schedule

@router.put("/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(schedule_id: int, schedule: schemas.ScheduleUpdate, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Расписание не найдено"
        )
    
    schedule_data = schedule.dict(exclude_unset=True)
    for key, value in schedule_data.items():
        setattr(db_schedule, key, value)
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Расписание не найдено"
        )
    
    db.delete(db_schedule)
    db.commit()
    return None 