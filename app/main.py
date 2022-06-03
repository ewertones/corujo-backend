from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models import models
from crud import assets as crud_assets, users as crud_users
from schemas import users, assets, asset_predictions, asset_values
from database.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health_check(db: Session = Depends(get_db)):
    return {"data": "Connected"}


@app.get("/users/", response_model=list[users.Users])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_users.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=users.Users)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_users.get_user(db, user_id)
    return user


@app.post("/users/", response_model=users.Users)
def create_user(user: users.UsersCreate, db: Session = Depends(get_db)):
    user = crud_users.get_user_by_email(db, email=user.email)
    if user:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    return crud_users.create_user(db, user)


# def generate_password_reset_token(email: str) -> str:
#     delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
#     now = datetime.utcnow()
#     expires = now + delta
#     exp = expires.timestamp()
#     encoded_jwt = jwt.encode(
#         {"exp": exp, "nbf": now, "sub": email},
#         settings.SECRET_KEY,
#         algorithm="HS256",
#     )
#     return encoded_jwt
