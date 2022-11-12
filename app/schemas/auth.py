from pydantic import BaseModel, EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False
