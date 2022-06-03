from datetime import date
from pydantic import BaseModel


class AssetValuesBase(BaseModel):
    asset_id: int
    date: date
    _open: float
    close: float
    high: float
    low: float
    volume: float


class AssetValuesCreate(AssetValuesBase):
    pass


class AssetValues(AssetValuesBase):
    id: int

    class Config:
        orm_mode = True
