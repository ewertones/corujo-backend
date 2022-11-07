from sqlalchemy.orm import Session
from models import models
from passlib.context import CryptContext
from schemas import users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return (
        db.query(models.Users)
        .with_entities(
            models.Users.email, models.Users.first_name, models.Users.last_name
        )
        .filter(models.Users.id == user_id)
        .first()
    )


def delete_user(db: Session, user_id: int):
    db.query(models.Users).filter(models.Users.id == user_id).delete()
    db.commit()
    return {"ok": True}


def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = (
        db.query(models.Users)
        .with_entities(
            models.Users.email, models.Users.first_name, models.Users.last_name
        )
        .order_by(models.Users.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return users


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
    return {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "birthday": user.birthday,
    }


def update_user(db: Session, user_id: int, new_info: users.UserUpdate):
    stored_data = db.get(models.Users, user_id)
    new_data = new_info.dict(exclude_unset=True)
    for key, value in new_data.items():
        setattr(stored_data, key, value)
    db.add(stored_data)
    db.commit()
    db.refresh(stored_data)
    return stored_data
