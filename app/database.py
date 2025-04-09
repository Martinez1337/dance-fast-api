from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import re
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Извлекаем имя базы данных из URL
pattern = r'postgresql(?:://|://)(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)/(?P<database>.+)'
match = re.match(pattern, DATABASE_URL)

if not match:
    raise ValueError(f"Некорректный формат DATABASE_URL: {DATABASE_URL}")

user = match.group('user')
password = match.group('password')
host = match.group('host')
port = match.group('port')
DATABASE_NAME = match.group('database')

def init_db():
    try:
        # Подключаемся к postgres для создания базы данных
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        with conn.cursor() as cur:
            # Проверяем существование базы данных
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DATABASE_NAME,))
            exists = cur.fetchone()
            
            if not exists:
                # Создаем базу данных
                cur.execute(f"CREATE DATABASE {DATABASE_NAME}")
                print(f"База данных {DATABASE_NAME} успешно создана")
            else:
                print(f"База данных {DATABASE_NAME} уже существует")
                
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        # В production не включайте password в логи
        print(f"Параметры подключения: user={user}, host={host}, port={port}, database={DATABASE_NAME}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

# Создаем движок для работы с нашей базой данных
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 