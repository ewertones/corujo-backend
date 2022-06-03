from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    NUMERIC,
    Table,
)
from sqlalchemy.orm import relationship
from database.database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birthday = Column(Date)
    remember_token = Column(String)
    is_active = Column(Boolean, default=True)
    wallet = relationship("Wallets", back_populates="user", uselist=False)


wallets_assets = Table(
    "wallets_assets",
    Base.metadata,
    Column("wallet_id", ForeignKey("wallets.id"), primary_key=True),
    Column("asset_id", ForeignKey("assets.id"), primary_key=True),
)


class Wallets(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    user = relationship("Users", back_populates="wallet")
    asset = relationship("Assets", secondary=wallets_assets, back_populates="wallet")


class Assets(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    _type = Column("type", String)
    description = Column(String)
    asset_values = relationship("AssetValues")
    asset_predictions = relationship("AssetPredictions")
    wallet = relationship("Wallets", secondary=wallets_assets, back_populates="asset")


class AssetValues(Base):
    __tablename__ = "asset_values"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset = relationship("Assets", back_populates="asset_values")
    date = Column(Date)
    _open = Column("open", NUMERIC(10, 2))
    close = Column(NUMERIC(10, 2))
    high = Column(NUMERIC(10, 2))
    low = Column(NUMERIC(10, 2))
    volume = Column(NUMERIC(10, 2))


class AssetPredictions(Base):
    __tablename__ = "asset_predictions"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset = relationship("Assets", back_populates="asset_predictions")
    date = Column(Date)
    _open = Column("open", NUMERIC(10, 2))
    close = Column(NUMERIC(10, 2))
    high = Column(NUMERIC(10, 2))
    low = Column(NUMERIC(10, 2))
    volume = Column(NUMERIC(10, 2))
