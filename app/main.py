from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models
from app.routers import users

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dance Studio API",
    description="API для мобильного приложения школы танцев",
    version="0.1.0"
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
app.include_router(users.router)

@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в API для школы танцев!",
        "docs": "/docs",
        "endpoints": [
            "/users"
        ]
    } 