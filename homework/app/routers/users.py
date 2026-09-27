from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, RefreshTokenSchema, UserUpdate
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
    require_admin,
    SECRET_KEY,
    ALGORITHM,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user_username = db.query(User).filter(User.username == user.username).first()

    if existing_user_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists")

    existing_user_email = db.query(User).filter(User.email == user.email).first()
    
    if existing_user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already exists")

    hashed_pwd = hash_password(user.password)
    data = user.model_dump(exclude={"password"})

    new_user = User(**data, hashed_password=hashed_pwd)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")

    access_token = create_access_token(data={"user_id": db_user.id})
    refresh_token = create_refresh_token(data={"user_id": db_user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }



@router.post("/token/refresh")
def refresh_token(request: RefreshTokenSchema):
    try:
        payload = jwt.decode(request.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        token_type = payload.get("token_type")

        if not user_id or token_type != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = create_access_token(data={"user_id": user_id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }



@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user



@router.patch("/me", response_model=UserResponse)
def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user_update.username and user_update.username != current_user.username:
        existing_username = db.query(User).filter(User.username == user_update.username).first()
        if existing_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in use")
        current_user.username = user_update.username

    if user_update.email and user_update.email != current_user.email:
        existing_email = db.query(User).filter(User.email == user_update.email).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        current_user.email = user_update.email

    db.commit()
    db.refresh(current_user)

    return current_user


@router.get("/", response_model=List[UserResponse])
def get_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    users = db.query(User).all()
    return users



@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user



@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": f"User {user.username} has been deleted"}