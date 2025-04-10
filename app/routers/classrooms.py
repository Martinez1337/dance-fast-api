from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

import uuid

router = APIRouter(
    prefix="/classrooms",
    tags=["classrooms"],
    responses={404: {"description": "Зал не найден"}}
    # dependencies=[Depends(get_current_active_user)]
)


@router.post("/", response_model=schemas.ClassroomBaseInfo, status_code=status.HTTP_201_CREATED)
def create_classroom(
        classroom_data: schemas.ClassroomBase,
        db: Session = Depends(get_db)
):
    classroom = models.Classroom(
        name=classroom_data.name,
        description=classroom_data.description,
        created_at=datetime.now(timezone.utc)
    )

    db.add(classroom)
    db.commit()
    db.refresh(classroom)

    return classroom


@router.get("/", response_model=List[schemas.ClassroomBaseInfo])
def get_all_classrooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    classrooms = db.query(models.Classroom).offset(skip).limit(limit).all()
    return classrooms


@router.get("/{classroom_id}", response_model=schemas.ClassroomBaseInfo)
def get_classroom_by_id(classroom_id: uuid.UUID, db: Session = Depends(get_db)):
    classroom = db.query(models.Classroom).filter(models.Classroom.id == classroom_id).first()
    if classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Зал не найден"
        )
    return classroom
