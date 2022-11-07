from datetime import date
from pydantic import BaseModel, Field


class AssetValueBase(BaseModel):
    asset_id: int
    date: date
    open: float = Field(alias="_open")
    close: float
    high: float
    low: float
    volume: float


class AssetValueCreate(AssetValueBase):
    pass


class AssetValueResponse(AssetValueBase):
    pass


class AssetValue(AssetValueBase):
    id: int

    class Config:
        orm_mode = True
