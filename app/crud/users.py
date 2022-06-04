from sqlalchemy.orm import Session
from models import models
from schemas import users


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()


def create_user(db: Session, user: users.UserCreate):
    hashed_password = user.password + "notreallyhashed"
    db_user = models.Users(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        birthday=user.birthday,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
