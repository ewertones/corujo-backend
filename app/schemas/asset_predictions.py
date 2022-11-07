from datetime import date
from pydantic import BaseModel, Field


class AssetPredictionBase(BaseModel):
    asset_id: int
    date: date
    open: float = Field(alias="_open")
    close: float
    high: float
    low: float
    volume: float


class AssetPredictionCreate(AssetPredictionBase):
    pass


class AssetPredictionResponse(AssetPredictionBase):
    pass


class AssetPrediction(AssetPredictionBase):
    id: int

    class Config:
        orm_mode = True
