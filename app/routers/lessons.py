import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import models, schemas
from app.auth.jwt import get_current_active_user, get_current_admin

router = APIRouter(
    prefix="/lessons",
    tags=["lessons"],
    responses={404: {"description": "Занятие не найдено"}}
)


@router.post("/", response_model=schemas.LessonBaseInfo, status_code=status.HTTP_201_CREATED)
async def create_lesson(lesson_data: schemas.LessonBase, db: Session = Depends(get_db)):
    lesson_type = db.query(models.LessonType).filter(models.LessonType.id == lesson_data.lesson_type_id).first()
    if not lesson_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Стиля танца с идентификатором {lesson_data.lesson_type_id} не существует",
        )

    classroom = db.query(models.Classroom).filter(models.Classroom.id == lesson_data.classroom_id).first()
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Зала с идентификатором {lesson_data.classroom_id} не существует",
        )

    group = db.query(models.Group).filter(models.Group.id == lesson_data.group_id).first()
    if not group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Группы с идентификатором {lesson_data.group_id} не существует",
        )

    lesson = models.Lesson(
        name=lesson_data.name,
        description=lesson_data.description,
        lesson_type_id=lesson_data.lesson_type_id,
        start_time=lesson_data.start_time,
        finish_time=lesson_data.finish_time,
        classroom_id=lesson_data.classroom_id,
        group_id=lesson_data.group_id
    )

    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    return lesson


@router.get("/", response_model=List[schemas.LessonBaseInfo])
async def get_all_lessons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lessons = db.query(models.Lesson).offset(skip).limit(limit).all()
    return lessons


@router.get("/full-info", response_model=List[schemas.LessonFullInfo])
async def get_all_lessons_full_info(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lessons = db.query(models.Lesson).offset(skip).limit(limit).all()
    return lessons


@router.get("/{lesson_id}", response_model=schemas.LessonBaseInfo)
async def get_lesson_by_id(lesson_id: uuid.UUID, db: Session = Depends(get_db)):
    lessons = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lessons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Занятие не найдено"
        )
    return lessons


@router.get("/full-info/{lessons_id}", response_model=schemas.LessonFullInfo)
async def get_lesson_full_info_by_id(lesson_id: uuid.UUID, db: Session = Depends(get_db)):
    lessons = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lessons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Занятие не найдено"
        )

    return lessons
