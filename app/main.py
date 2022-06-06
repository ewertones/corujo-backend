from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from passlib.context import CryptContext
from jose import jwt, JWTError

from models import models
from crud import assets as crud_assets, users as crud_users
from schemas import users, assets, asset_predictions, asset_values
from database.database import SessionLocal, engine

from datetime import datetime, timedelta

import os


FASTAPI_SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = crud_users.get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, FASTAPI_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, FASTAPI_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud_users.get_user_by_email(db=db, email=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: users.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inativo")
    return current_user


@app.get("/")
async def get_docs():
    return RedirectResponse("docs")


@app.post("/user", response_model=users.User)
def create_user(user: users.UserCreate, db: Session = Depends(get_db)):
    is_email_being_used = crud_users.get_user_by_email(db, email=user.email)
    if is_email_being_used:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    return crud_users.create_user(db, user)


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
def get_user_me(current_user: users.User = Depends(get_current_active_user)):
    return current_user


# @app.get("/users", response_model=list[users.User])
# def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud_users.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=users.User)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     user = crud_users.get_user(db, user_id)
#     return user

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
