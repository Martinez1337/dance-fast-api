from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base, init_db
# Явно импортируем все модели
from app.models.base import BaseModel
from app.models.user import User
from app.models.level import Level
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.admin import Admin
from app.models.group import Group
from app.models.lesson import Lesson
from app.models.classroom import Classroom
from app.models.lesson_type import LessonType
from app.models.slot import Slot
from app.models.subscription import Subscription
from app.models.subscription_template import SubscriptionTemplate
from app.models.payment import Payment
from app.models.payment_type import PaymentType
from app.models.event import Event
from app.models.event_type import EventType
from app.models.association import (
    TeacherLesson, TeacherGroup, StudentGroup,
    LessonSubscription, SubscriptionLessonType
)
from app.routers import users, auth, events, eventTypes
import os

print("Запуск приложения...")
print(f"DATABASE_URL в окружении: {os.getenv('DATABASE_URL')}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск события startup")
    try:
        # Создаем базу данных, если её нет
        init_db()

        # Создаем все таблицы
        # Base.metadata создаёт все таблицы из моделей, которые наследуются от Base
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Ошибка при инициализации: {e}")
    yield
    print("Завершение работы приложения")


app = FastAPI(
    title="Dance Studio API",
    description="API для мобильного приложения школы танцев",
    version="0.1.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(events.router)
app.include_router(eventTypes.router)


@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в API для школы танцев!",
        "docs": "/docs",
        "endpoints": [
            "/auth",
            "/users"
            "/events"
            "/eventTypes"
        ]
    }
