from datetime import date
from pydantic import BaseModel


class UsersBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    birthday: date = date(2000, 1, 1)


class UsersCreate(UsersBase):
    password: str


class Users(UsersBase):
    id: int
    remember_token: str | None = None
    is_active: bool = False

    class Config:
        orm_mode = True
