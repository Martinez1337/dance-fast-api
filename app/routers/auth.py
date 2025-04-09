from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone

from app.database import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.models.student import Student
from app.models.level import Level
from app.auth.password import verify_password, get_password_hash
from app.auth.jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя."""
    # Проверяем, существует ли пользователь с таким email
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    # Создаем нового пользователя
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        middle_name=user_data.middle_name,
        description=user_data.description,
        phone_number=user_data.phone_number,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    new_user.role = "student"
    new_user.level_name = db.query(Level).filter(Level.id == user_data.level_id).first().name
    
    # Сохраняем пользователя в базе данных
    db.add(new_user)
    db.commit()

    # Создаем запись в таблице student
    student = Student(
        user_id=new_user.id,
        level_id=user_data.level_id,
        created_at=new_user.created_at
    )   
    db.add(student)
    db.commit()
    
    db.refresh(new_user)
    db.refresh(student)

    db.close()
    return new_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Получение токена доступа."""
    # Ищем пользователя по email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Проверяем учетные данные пользователя
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем данные для токена
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Получение данных текущего пользователя."""
    return current_user 