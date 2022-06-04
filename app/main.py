from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from models import models
from crud import assets as crud_assets, users as crud_users
from schemas import users, assets, asset_predictions, asset_values
from database.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from datetime import date


def fake_hash_password(password):
    return password + "notreallyhashed"


def fake_decode_token(token):
    return users.User(
        email=token + "fakedecoded",
        first_name="Teste",
        last_name="Token",
        birthday=date(2022, 6, 3),
        id=1,
        is_active=True,
        is_superuser=True,
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais invalidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: users.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inativo")
    return current_user


@app.get("/")
async def get_docs():
    return RedirectResponse("docs")


@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud_users.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario ou senha incorretos")
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Usuario ou senha incorretos")

    return {"access_token": user.email, "token_type": "bearer"}


@app.get("/auth")
def token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return {"data": "Connected", "token": token}


@app.get("/users", response_model=list[users.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_users.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/me")
def get_user_me(current_user: users.User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/{user_id}", response_model=users.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_users.get_user(db, user_id)
    return user


@app.post("/users", response_model=users.User)
def create_user(user: users.UserCreate, db: Session = Depends(get_db)):
    is_email_being_used = crud_users.get_user_by_email(db, email=user.email)
    if is_email_being_used:
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
