from pydantic import BaseModel, Field
from datetime import date


class AssetBase(BaseModel):
    name: str
    type: str = Field(alias="_type")
    description: str


class AssetCreate(AssetBase):
    pass


class Asset(AssetBase):
    id: int
    symbol: str

    class Config:
        orm_mode = True


class AssetFeed(BaseModel):
    name: str
    symbol: str
    currency: str
    close: float
    diff: float
    diff_percent: float
    date: date
