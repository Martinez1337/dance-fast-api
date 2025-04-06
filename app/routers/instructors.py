from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/instructors",
    tags=["instructors"],
    responses={404: {"description": "Инструктор не найден"}},
)

@router.post("/", response_model=schemas.Instructor, status_code=status.HTTP_201_CREATED)
def create_instructor(instructor: schemas.InstructorCreate, db: Session = Depends(get_db)):
    db_instructor = models.Instructor(**instructor.dict())
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

@router.get("/", response_model=List[schemas.Instructor])
def read_instructors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    instructors = db.query(models.Instructor).offset(skip).limit(limit).all()
    return instructors

@router.get("/{instructor_id}", response_model=schemas.Instructor)
def read_instructor(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if db_instructor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Инструктор не найден"
        )
    return db_instructor

@router.put("/{instructor_id}", response_model=schemas.Instructor)
def update_instructor(instructor_id: int, instructor: schemas.InstructorUpdate, db: Session = Depends(get_db)):
    db_instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if db_instructor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Инструктор не найден"
        )
    
    instructor_data = instructor.dict(exclude_unset=True)
    for key, value in instructor_data.items():
        setattr(db_instructor, key, value)
    
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

@router.delete("/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    db_instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if db_instructor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Инструктор не найден"
        )
    
    db.delete(db_instructor)
    db.commit()
    return None 