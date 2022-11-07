from datetime import datetime
from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class AuthMessage(BaseModel):
    access_token: str
    token_type: str


class HTTPError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
