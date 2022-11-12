from re import A
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.param_functions import Form

from typing import Optional

from sqlalchemy.orm import Session

from passlib.context import CryptContext
from jose import jwt, JWTError

from models import models
from crud import assets as crud_assets, users as crud_users
from schemas import users, assets, asset_predictions, asset_values, auth
from schemas.messages import Message, HTTPError, AuthMessage
from database.database import SessionLocal, engine

from datetime import date, datetime, timedelta

import os


FASTAPI_SECRET_KEY = os.getenv("FASTAPI_SECRET_KEY")
ALGORITHM = "HS256"
models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI(
    title="Corujo API",
    description="Te permite realizar as mesmas ações que você faria na UI.",
    version="0.1.0",
    terms_of_service="https://corujo.com.br/termos",
    contact={
        "name": "Ewerton Souza",
        "email": "admin@corujo.com.br",
    },
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

origins = [
    "http://corujo.com.br",
    "https://corujo.com.br",
    "http://www.corujo.com.br",
    "https://www.corujo.com.br",
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


def authenticate_user(db: Session, email: str, password: str):
    user = crud_users.get_user_by_email(db, email)
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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")


@app.get("/")
@app.get("/docs", include_in_schema=False)
async def get_docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        swagger_favicon_url="favicon.ico",
    )


@app.post(
    "/login",
    responses={
        200: {"model": AuthMessage},
        401: {
            "model": HTTPError,
            "description": "This endpoint always raises an error",
        },
    },
    tags=["user"],
)
async def login(
    form_data: auth.Login,
    db: Session = Depends(get_db),
):
    access_token_expires = (
        timedelta(days=30) if form_data.remember_me else timedelta(minutes=60)
    )

    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "valid_until": datetime.now() + access_token_expires,
    }


@app.get("/user", response_model=users.UserResponse, tags=["user"])
def get_my_profile(current_user: users.User = Depends(get_current_active_user)):
    return {
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
    }


@app.patch("/user", response_model=users.User, tags=["user"])
def patch_my_profile(
    new_info: users.UserUpdate,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return crud_users.update_user(db, current_user.id, new_info)


@app.delete("/user", tags=["user"])
def delete_my_profile(
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return crud_users.delete_user(db, current_user.id)


@app.post(
    "/email",
    responses={
        200: {"model": Message},
        409: {
            "model": HTTPError,
            "description": "This endpoint always raises an error",
        },
    },
    tags=["user"],
)
async def is_email_already_on_db(email: users.UserEmail, db: Session = Depends(get_db)):
    if is_email_being_used := crud_users.get_user_by_email(db, email=email.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado."
        )
    else:
        return {"message": "Email disponível."}


@app.post(
    "/user",
    response_model=users.UserBase,
    responses={
        201: {"model": users.UserBase},
        409: {
            "model": HTTPError,
            "description": "Email já cadastrado.",
        },
    },
    status_code=201,
    tags=["user"],
)
def create_user(
    user: users.UserCreate,
    db: Session = Depends(get_db),
):
    is_email_being_used = crud_users.get_user_by_email(db, email=user.email)
    if is_email_being_used:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado."
        )

    return crud_users.create_user(db, user)


@app.get("/users", response_model=list[users.UserResponse], tags=["admin"])
def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.is_superuser:
        return crud_users.get_users(db, skip, limit)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não tem permissão para executar tal ação.",
        )


@app.get(
    "/user/{user_id}",
    response_model=users.UserResponse,
    responses={
        200: {"model": users.UserResponse},
        401: {
            "model": HTTPError,
            "description": "Você não tem permissão para executar tal ação.",
        },
        404: {
            "model": HTTPError,
            "description": "Usuário não encontrado.",
        },
    },
    tags=["admin"],
)
def get_user(
    user_id: int,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.is_superuser:
        if existing_user := crud_users.get_user(db, user_id):
            return existing_user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não tem permissão para executar tal ação.",
        )


@app.patch("/user/{user_id}", response_model=users.User, tags=["admin"])
def patch_user(
    user_id: int,
    new_info: users.UserUpdate,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.is_superuser:
        return crud_users.update_user(db, user_id, new_info)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não tem permissão para executar tal ação.",
        )


@app.delete("/user/{user_id}", tags=["admin"])
def delete_user(
    user_id: int,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.is_superuser:
        return crud_users.delete_user(db, user_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não tem permissão para executar tal ação.",
        )


@app.get("/asset/{asset_id}", response_model=assets.Asset, tags=["user"])
def get_asset(
    asset_id: int,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return crud_assets.get_asset(db, asset_id)


@app.get("/assets", response_model=list[assets.Asset], tags=["user"])
def get_assets(
    skip: int = 0,
    limit: int = 100,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return crud_assets.get_assets(db, skip=skip, limit=limit)


@app.get(
    "/asset/{asset_id}/prediction/{date}",
    response_model=asset_predictions.AssetPredictionResponse,
    tags=["user"],
)
def get_asset_prediction(
    asset_id: int,
    date: date,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return crud_assets.get_asset_prediction(db, asset_id, date)


@app.get(
    "/asset/{asset_id}/predictions",
    response_model=list[asset_predictions.AssetPredictionResponse],
    tags=["admin"],
)
def get_asset_predictions(
    asset_id: int,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    if current_user.is_superuser:
        return crud_assets.get_asset_predictions(db, asset_id, skip, limit)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não tem permissão para executar tal ação.",
        )


@app.get(
    "/asset/{asset_id}/value/{date}",
    response_model=asset_values.AssetValueResponse,
    tags=["user"],
)
def get_asset_value(
    asset_id: int,
    date: date,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return crud_assets.get_asset_value(db, asset_id, date)


@app.get(
    "/asset/{asset_id}/values",
    response_model=list[asset_values.AssetValueResponse],
    tags=["admin"],
)
def get_asset_values(
    asset_id: int,
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    if current_user.is_superuser:
        return crud_assets.get_asset_values(db, asset_id, skip, limit)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não tem permissão para executar tal ação.",
        )


@app.get("/assets/feed", response_model=list[assets.AssetFeed], tags=["user"])
def get_assets_feed(
    current_user: users.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return crud_assets.get_assets_feed(db)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
