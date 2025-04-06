from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/dance-classes",
    tags=["dance classes"],
    responses={404: {"description": "Класс не найден"}},
)

@router.post("/", response_model=schemas.DanceClass, status_code=status.HTTP_201_CREATED)
def create_dance_class(dance_class: schemas.DanceClassCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли инструктор
    instructor = db.query(models.Instructor).filter(models.Instructor.id == dance_class.instructor_id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Инструктор не найден"
        )
    
    db_dance_class = models.DanceClass(**dance_class.dict())
    db.add(db_dance_class)
    db.commit()
    db.refresh(db_dance_class)
    return db_dance_class

@router.get("/", response_model=List[schemas.DanceClass])
def read_dance_classes(
    skip: int = 0, 
    limit: int = 100, 
    style: Optional[str] = None, 
    level: Optional[str] = None,
    instructor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.DanceClass)
    
    if style:
        query = query.filter(models.DanceClass.style == style)
    if level:
        query = query.filter(models.DanceClass.level == level)
    if instructor_id:
        query = query.filter(models.DanceClass.instructor_id == instructor_id)
    
    dance_classes = query.offset(skip).limit(limit).all()
    return dance_classes

@router.get("/{dance_class_id}", response_model=schemas.DanceClass)
def read_dance_class(dance_class_id: int, db: Session = Depends(get_db)):
    db_dance_class = db.query(models.DanceClass).filter(models.DanceClass.id == dance_class_id).first()
    if db_dance_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Класс не найден"
        )
    return db_dance_class

@router.put("/{dance_class_id}", response_model=schemas.DanceClass)
def update_dance_class(dance_class_id: int, dance_class: schemas.DanceClassUpdate, db: Session = Depends(get_db)):
    db_dance_class = db.query(models.DanceClass).filter(models.DanceClass.id == dance_class_id).first()
    if db_dance_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Класс не найден"
        )
    
    # Проверяем инструктора, если он был обновлен
    if dance_class.instructor_id:
        instructor = db.query(models.Instructor).filter(models.Instructor.id == dance_class.instructor_id).first()
        if not instructor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Инструктор не найден"
            )
    
    dance_class_data = dance_class.dict(exclude_unset=True)
    for key, value in dance_class_data.items():
        setattr(db_dance_class, key, value)
    
    db.commit()
    db.refresh(db_dance_class)
    return db_dance_class

@router.delete("/{dance_class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dance_class(dance_class_id: int, db: Session = Depends(get_db)):
    db_dance_class = db.query(models.DanceClass).filter(models.DanceClass.id == dance_class_id).first()
    if db_dance_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Класс не найден"
        )
    
    db.delete(db_dance_class)
    db.commit()
    return None 