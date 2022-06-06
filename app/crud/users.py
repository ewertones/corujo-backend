from sqlalchemy.orm import Session
from models import models
from schemas import users
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_user(db: Session, user: users.UserCreate):
    db_user = models.Users(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        birthday=user.birthday,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
