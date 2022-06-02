from sqlalchemy.orm import Session
import models.models as models
import schemas.users as users


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def create_user(db: Session, user: users.UsersCreate):
    fake_hashed_password = user.hashed_password + "notreallyhashed"
    db_user = models.Users(
        email=user.email,
        hashed_password=user.hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        birthday=user.birthday,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
