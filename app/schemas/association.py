import uuid
from pydantic import BaseModel
from app.schemas.level import LevelBaseInfo
from app.schemas.student import StudentFullInfo
from app.schemas.teacher import TeacherFullInfo
from datetime import datetime
from typing import Optional, List


class StudentGroupBase(BaseModel):
    student: StudentFullInfo
    join_date: datetime

    class Config:
        from_attributes = True


class TeacherGroupBase(BaseModel):
    teacher: TeacherFullInfo

    class Config:
        from_attributes = True
