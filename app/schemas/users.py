from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UsersBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    birthday: datetime


class UsersCreate(UsersBase):
    hashed_password: str


class Users(UsersBase):
    id: int
    remember_token: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True
