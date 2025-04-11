import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.auth.jwt import get_current_active_user, get_current_admin

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Студент не найден"}}
)


@router.post("/", response_model=schemas.StudentBaseInfo, status_code=status.HTTP_201_CREATED)
async def create_student(
        student_data: schemas.StudentBase,
        db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == student_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователя с идентификатором {student_data.user_id} не существует",
        )

    level = db.query(models.Level).filter(models.Level.id == student_data.level_id).first()
    if not level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Уровня подготовки с идентификатором {student_data.level_id} не существует",
        )

    student = models.Student(
        user_id=student_data.user_id,
        level_id=student_data.level_id,
        created_at=datetime.now(timezone.utc)
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


@router.get("/", response_model=List[schemas.StudentBaseInfo])
async def get_all_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students


@router.get("/full-info", response_model=List[schemas.StudentFullInfo])
async def get_all_students_full_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(models.Student).offset(skip).limit(limit).all()

    students_full_info = []

    for student in students:
        student_full_info = get_student_full_info_by_id(student.id)
        students_full_info.append(student_full_info)

    return students


@router.get("/{student_id}", response_model=schemas.StudentBaseInfo)
async def get_student_by_id(student_id: uuid.UUID, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент не найден"
        )
    return student


@router.get("/full-info/{student_id}", response_model=schemas.StudentFullInfo)
async def get_student_full_info_by_id(student_id: uuid.UUID, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Студент не найден"
        )

    user = db.query(models.User).filter(models.User.id == student.user_id).first()
    level = db.query(models.Level).filter(models.Level.id == student.level_id).first()

    student_full_info = schemas.StudentFullInfo(
        id=student.id,
        user_id=student.user_id,
        level_id=student.level_id,
        created_at=student.created_at,
        terminated=student.terminated,
        user=schemas.UserBase(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            description=user.description,
            phone_number=user.phone_number,
        ),
        level=schemas.LevelBaseInfo(
            id=level.id,
            name=level.name,
            description=level.description,
            terminated=level.terminated
        )
    )

    return student_full_info
