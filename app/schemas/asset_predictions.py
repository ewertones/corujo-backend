from datetime import date
from pydantic import BaseModel


class AssetPredictionsBase(BaseModel):
    asset_id: int
    date: date
    _open: float
    close: float
    high: float
    low: float
    volume: float


class AssetPredictionsCreate(AssetPredictionsBase):
    pass


class AssetPredictions(AssetPredictionsBase):
    id: int

    class Config:
        orm_mode = True
