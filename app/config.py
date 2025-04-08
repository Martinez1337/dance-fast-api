import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Загрузка переменных окружения из файла .env
load_dotenv()

class Settings(BaseSettings):
    # Настройки базы данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/dance_api")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "dance_api")
    # Настройки приложения
    APP_NAME: str = os.getenv("APP_NAME", "Dance Studio API")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Настройки сервера
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Создание экземпляра настроек
settings = Settings() 