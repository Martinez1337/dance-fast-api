from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
    responses={404: {"description": "Бронирование не найдено"}},
)

@router.post("/", response_model=schemas.Booking, status_code=status.HTTP_201_CREATED)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь
    user = db.query(models.User).filter(models.User.id == booking.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    # Проверяем, существует ли расписание
    schedule = db.query(models.Schedule).filter(models.Schedule.id == booking.schedule_id).first()
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Расписание не найдено"
        )
    
    # Проверяем, есть ли свободные места
    if schedule.current_enrolled >= schedule.max_capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет свободных мест на данное занятие"
        )
    
    # Проверяем, не записан ли пользователь уже на это занятие
    existing_booking = db.query(models.Booking).filter(
        models.Booking.user_id == booking.user_id,
        models.Booking.schedule_id == booking.schedule_id,
        models.Booking.status != "cancelled"
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже записан на это занятие"
        )
    
    # Создаем бронирование
    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    
    # Увеличиваем количество записанных людей
    schedule.current_enrolled += 1
    
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.get("/", response_model=List[schemas.Booking])
def read_bookings(
    skip: int = 0, 
    limit: int = 100, 
    user_id: Optional[int] = None,
    schedule_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Booking)
    
    if user_id:
        query = query.filter(models.Booking.user_id == user_id)
    if schedule_id:
        query = query.filter(models.Booking.schedule_id == schedule_id)
    if status:
        query = query.filter(models.Booking.status == status)
    
    bookings = query.offset(skip).limit(limit).all()
    return bookings

@router.get("/{booking_id}", response_model=schemas.Booking)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Бронирование не найдено"
        )
    return db_booking

@router.put("/{booking_id}", response_model=schemas.Booking)
def update_booking(booking_id: int, booking: schemas.BookingUpdate, db: Session = Depends(get_db)):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Бронирование не найдено"
        )
    
    # Если статус меняется на "cancelled", уменьшаем количество записанных людей
    if booking.status == "cancelled" and db_booking.status != "cancelled":
        schedule = db.query(models.Schedule).filter(models.Schedule.id == db_booking.schedule_id).first()
        if schedule and schedule.current_enrolled > 0:
            schedule.current_enrolled -= 1
    
    booking_data = booking.dict(exclude_unset=True)
    for key, value in booking_data.items():
        setattr(db_booking, key, value)
    
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if db_booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Бронирование не найдено"
        )
    
    # Если бронирование не отменено, уменьшаем количество записанных людей
    if db_booking.status != "cancelled":
        schedule = db.query(models.Schedule).filter(models.Schedule.id == db_booking.schedule_id).first()
        if schedule and schedule.current_enrolled > 0:
            schedule.current_enrolled -= 1
    
    db.delete(db_booking)
    db.commit()
    return None 