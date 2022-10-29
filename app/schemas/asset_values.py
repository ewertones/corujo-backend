from datetime import date
from pydantic import BaseModel


class AssetValueBase(BaseModel):
    asset_id: int
    date: date
    _open: float
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
