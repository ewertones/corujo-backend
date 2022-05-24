from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from passlib import hash
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(Date)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    remember_token = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = 