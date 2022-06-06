from datetime import date, datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    birthday: date


class UserCreate(UserBase):
    password: str


class UserInDBBase(UserBase):
    id: int
    remember_token: str | None = None
    is_active: bool = False
    is_superuser: bool = False
    created_at: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str